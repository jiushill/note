using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using Amib.Threading;
using System.Net;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Windows.Forms;

namespace fofa_query
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            threadsetfunc();
            responseload();
        }

        private static  SmartThreadPool stp = new SmartThreadPool(); //定义线程池
        private static string querystr=""; //返回的查询语法记录
        private static int numberip = 0; //收集的IP数量
        private static List<string> urls = new List<string>();
        private static int tmppage = 0;

        private static void stopthreadpool()
        {
            stp.Cancel();
        }

        //多线程设置
        private void threadsetfunc() {
            int[] threadlist = { 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 200 };
            foreach (var td in threadlist) {
                threadset.Items.Add(td);
            }
        }

        //返回内存UI设置
        private void responseload() {
            response.GridLines = true;
            response.FullRowSelect = true;
            response.View = View.Details;
            response.Scrollable = true;
            response.MultiSelect = true;
            response.Columns.Add("IP", 160, HorizontalAlignment.Center);
            response.Columns.Add("URL", 160, HorizontalAlignment.Center);
            response.Columns.Add("PORT", 160, HorizontalAlignment.Center);
        }

        //异步委托
        public class Query {
            public delegate void Updateui(string ip,string url,string port);
            public Updateui update;
            public delegate void Out();
            public Out outs;

            public void stop() {
                while (true) {
                    if (stp.IsIdle == true) {
                        break;
                    }
                }
                outs();
            }
            public void query(string url)
            {
                    try
                    {
                        tmppage += 1;
                        HttpWebRequest requests = (HttpWebRequest)WebRequest.Create(url);
                        requests.Method = "GET";
                        requests.Headers.Add("UserAgent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36");
                        HttpWebResponse response = (HttpWebResponse)requests.GetResponse();
                        StreamReader sr = new StreamReader(response.GetResponseStream(), Encoding.GetEncoding("utf-8"));
                        string html = sr.ReadToEnd();
                        var Name = JObject.Parse(html);
                        string error = Name["error"].ToString();
                        string resultquery = Name["query"].ToString().Replace("\\", "");
                        querystr = resultquery;
                        if (error != "false")
                        {
                            if (Name["results"].Count() != 0)
                            {
                                foreach (var result in Name["results"])
                                {
                                    string url_ = result[0].ToString();
                                    string ip = result[1].ToString();
                                    string port = result[2].ToString();
                                    numberip += 1;
                                    update(ip, url_, port);
                                }
                            }
                            else
                            {
                                update("", "", "");
                            }
                        }
                        else
                        {
                            update("", "", "");
                        }
                    }
                    catch (WebException Ex)
                    {
                        MessageBox.Show("请求出现异常:" + Ex.ToString());
                        stopthreadpool();
                    }
            }
        }

        //开始或暂停
        private void button1_Click(object sender, EventArgs e)
        {

            //恢复初始化
            numberip = 0;
            tmppage = 0;
            urls.Clear();
            Query q = new Query();
            q.update += updateUI;
            q.outs += outs;
            label10.Text = "当前页数:0/0";
            if (button1.Text == "停止")
            {
                stp.Cancel(true);
                button1.Text = "开始";
                button1.Refresh();
            }
            else
            {
                if (email.TextLength != 0 && key.TextLength != 0 && search.TextLength != 0 && page.TextLength != 0)
                {
                    label10.Text = "当前页数:0/" + page.Text.ToString();
                    button1.Text = "停止";
                    string search_base64 = Convert.ToBase64String(Encoding.UTF8.GetBytes(search.Text.ToString())).Replace("+", "%2b");
                    stp.MaxQueueLength = Convert.ToInt32(threadset.Text.ToString());
                    for (int p = 0; p < Convert.ToInt32(page.Text.ToString()); p++)
                    {
                        string fofaurl = "https://fofa.so/api/v1/search/all?email=" + email.Text.ToString() + "&key=" + key.Text.ToString() + "&qbase64=" + search_base64 + "&page=" + p;
                        stp.QueueWorkItem<string>(q.query, fofaurl);
                    }
                }
                else
                {
                    MessageBox.Show("检查邮箱/key/搜索语法/页面是否填写错误");
                }
                SmartThreadPool tmp = new SmartThreadPool();
                tmp.QueueWorkItem(q.stop);
            }

        }

        delegate void asyncupdate(string ip, string url, string port);
        delegate void Outs();
        //更新UI
        private void updateUI(string ip, string url, string port) {
            if (InvokeRequired)
            {
                this.Invoke(new asyncupdate(delegate (string ip_, string url_, string port_)
                {
                    label10.Text = "页数:" + tmppage + "/" + page.Text.ToString();
                    label10.Refresh();
                    label9.Text = "查询语法为:" + querystr.ToString();
                    label9.Refresh();
                    if (ip.Length != 0 && port.Length != 0)
                    {
                        ListViewItem item = new ListViewItem();
                        item.SubItems.Clear();
                        item.SubItems[0].Text = ip;
                        item.SubItems.Add(url);
                        item.SubItems.Add(port);
                        response.Items.Add(item);
                        label6.Text = "已收集的IP数量:" + numberip.ToString();
                        label6.Refresh();
                        response.Items[response.Items.Count - 1].EnsureVisible();
                    }
                }), ip, url, port);

            }
            else {
                label10.Text = "页数:" + tmppage + "/" + page.Text.ToString();
                label10.Refresh();
                label9.Text = "查询语法为:" + querystr.ToString();
                label9.Refresh();
                if (ip.Length != 0 && port.Length != 0)
                {
                    ListViewItem item = new ListViewItem();
                    item.SubItems.Clear();
                    item.SubItems[0].Text = ip;
                    item.SubItems.Add(url);
                    item.SubItems.Add(port);
                    response.Items.Add(item);
                    label6.Text = "已收集的IP数量:" + numberip.ToString();
                    label6.Refresh();
                    response.Items[response.Items.Count - 1].EnsureVisible();
                }
            }
        }

        //任务完成
        private void outs() {
            if (InvokeRequired)
            {
                this.Invoke(new Outs(delegate ()
                {
                    button1.Text = "开始";
                    button1.Refresh();
                    MessageBox.Show("任务完成");
                }));
            }
            else {
                this.Invoke(new Outs(delegate ()
                {
                    button1.Text = "开始";
                    button1.Refresh();
                    MessageBox.Show("任务完成");
                }));
            }
        }

        //限制page只能输入数字
        private void page_KeyPress(object sender, KeyPressEventArgs e)
        {
                if (!(Char.IsNumber(e.KeyChar)) && e.KeyChar != (char)13 && e.KeyChar != (char)8){
                    e.Handled = true;
                }
        }

        //清空获取的结果
        private static void deleteitems(ListView datasx) {
            for (int c = 0; c < datasx.Items.Count; c++) {
                datasx.Items.RemoveAt(c);
            }

            for (int c = 0; c < datasx.Items.Count; c++)
            {
                deleteitems(datasx);
            }
        }

        private void 保存到文件ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var savedialog = new System.Windows.Forms.SaveFileDialog();
            savedialog.Filter = "txt (*.txt)|*.txt";
            savedialog.FileName = "save.txt";
            savedialog.ShowDialog();
            FileStream f = new FileStream(savedialog.FileName,FileMode.Create);
            StreamWriter fw = new StreamWriter(f);
            for (int calc = 0; calc < response.Items.Count; calc++) {
                var d = response.Items[calc].SubItems;
                string ip = d[0].Text;
                string url = d[1].Text;
                string port = d[2].Text;
                string output = "IP:" + ip + " url:" + url + " port:" + port;
                fw.WriteLine(output);
            }
            fw.Close();
            f.Close();
            MessageBox.Show("文件保存在:"+savedialog.FileName);
        }

        private void 复制所选ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var selectdata = response.SelectedItems;
            var d = response.Items[0].SubItems;
            string ip = d[0].Text;
            string url = d[1].Text;
            string port = d[2].Text;
            string output = "IP:" + ip + " url:" + url + " port:" + port;
            MessageBox.Show(output);
            Clipboard.SetDataObject(output);
        }

        private void 清空ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            deleteitems(response);
        }
    }
}
