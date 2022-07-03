using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Net.Http;
using System.Threading;
using System.Diagnostics;
using System.IO;
using HtmlAgilityPack;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;

namespace fofa_query
{
    public partial class Form1 : Form
    {
        public static Form1 form1;
        public static string searchurl;
        public static string searchtext;
        public static string cookies;
        public static int page;
        public static int sleeptime;

        public Form1()
        {
            InitializeComponent();
            timesleep.Text=timesleep.Items[2].ToString();
            sleeptime = Int32.Parse(timesleep.Text);
            savebutton.Enabled = false;
            for (int calc = 0; calc < savelist.Items.Count; calc++) {
                savelist.SetItemChecked(calc,true);
            }
            form1 = this;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void contextMenuStrip2_Opening(object sender, CancelEventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        public static void buttonstop(int id)
        {
            if (id == 0)
            {
                fofa_query.Form1.form1.querybox.Invoke(new Action(() =>
                {
                    fofa_query.Form1.form1.querybox.Enabled = false;
                }));
            }
            else {
                fofa_query.Form1.form1.querybox.Invoke(new Action(() =>
                {
                    fofa_query.Form1.form1.querybox.Enabled = true;
                }));

            }
        }

        private void querybox_Click(object sender, EventArgs e)
        {
            int errorid = 0;
            page=0;
            searchurl = searchcurl.Text;
            searchtext = Convert.ToBase64String(Encoding.UTF8.GetBytes(searchbox.Text)).Replace("=","%3D");
            cookies = cookiebox.Text;
            try
            {
                page =int.Parse(pagebox.Text);
            }
            catch {
                errorid = 1;
                MessageBox.Show("page不是数字");
            }

            if (errorid != 1)
            {
                ThreadStart thStat = new ThreadStart(fofa_search.start);
                Thread thread = new Thread(thStat);
                thread.Priority = ThreadPriority.Highest;
                thread.IsBackground = true;
                thread.Start();
                
            }
        }


        private void savebutton_Click(object sender, EventArgs e)
        {
            string result = "";
            List<string> tmparray = new List<string>();
            var savelist = fofa_query.Form1.form1.savelist.Items;
            for (int tmp = 0; tmp < savelist.Count; tmp++) {
                if (fofa_query.Form1.form1.savelist.GetItemChecked(tmp)) {
                    tmparray.Add(savelist[tmp].ToString());
                }
            }

            var resultlist = fofa_query.Form1.form1.resultlistview.Items;
            for (int calc = 0; calc < resultlist.Count; calc++) {
                string title = resultlist[calc].SubItems[0].Text;
                string url = resultlist[calc].SubItems[1].Text;
                string ip = resultlist[calc].SubItems[2].Text;
                string port = resultlist[calc].SubItems[3].Text;
                string nation = resultlist[calc].SubItems[4].Text;
                string area = resultlist[calc].SubItems[5].Text;
                if (tmparray.Contains("title")) {
                    result += title;
                }

                if (tmparray.Contains("url")) {
                    result +=" "+url;
                }

                if (tmparray.Contains("ip")) {
                    result += " "+ip;
                }

                if (tmparray.Contains("port")) {
                    result +=" "+port;
                }

                if (tmparray.Contains("nation")) {
                    result += " " + nation;
                }

                if (tmparray.Contains("area")) {
                    result += " " + area;
                }
                result += "\n";
            }
            File.WriteAllText("save.txt", result);
            MessageBox.Show("结果已保存到save.txt");
        }

        private void importbutton_Click(object sender, EventArgs e)
        {
            if (File.Exists("config.txt"))
            {
                string[] config = File.ReadAllText("config.txt").Split('\n');
                try
                {
                    string url = config[0].Replace("[url]=","").Replace("\r","");
                    string cookie = config[1].Replace("[cookie]=", "").Replace("\r", "");
                    string search = config[2].Replace("[search]=", "").Replace("\r", "");
                    searchcurl.Text = url;
                    cookiebox.Text = cookie;
                    searchbox.Text = search;
                }
                catch {
                    MessageBox.Show("config.txt格式不正确") ;
                }
            }
            else {
                MessageBox.Show("当前目录不存在config.txt");
            }
        }

        private void clearbutton_Click(object sender, EventArgs e)
        {
            resultlistview.Items.Clear();
        }
        public class fofa_search
        {

            public static void start()
            {
                fofa_query.Form1.buttonstop(0);
                string cookie = fofa_query.Form1.cookies;
                string url = fofa_query.Form1.searchurl;
                int page = fofa_query.Form1.page;
                string search = fofa_query.Form1.searchtext;
                int timesleep = fofa_query.Form1.sleeptime;
                fofa_query.Form1.form1.timesleep.Invoke(new Action(() => {
                   timesleep=Int32.Parse(fofa_query.Form1.form1.timesleep.Text);
                }));
                try
                {
                    for (int calc = 1; calc < page+1; calc++)
                    {
                        string url2 = string.Format(url, searchtext, calc.ToString()); //要爬取的url生成
                        Debug.Print(url2);
                        HttpClientHandler header = new HttpClientHandler() { UseCookies = false };
                        HttpClient request = new HttpClient(header);
                        HttpRequestMessage message = new HttpRequestMessage(HttpMethod.Get, url2);
                        message.Headers.Add("KeepAlive", "true");
                        message.Headers.Add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36");
                        message.Headers.Add("Accept", "*/*");
                        message.Headers.Add("Cookie", cookie);
                        var task = Task.Run(async () =>
                       {
                           Thread.Sleep(timesleep);
                           var result = await request.SendAsync(message);
                           if (result.StatusCode.GetHashCode() == 406)
                           {
                               fofa_query.Form1.form1.errortext.Invoke(new Action(() =>
                               {
                                   fofa_query.Form1.form1.errortext.Text = "捕获异常：请求过快状态码406";
                               }));
                           }
                           else {
                               fofa_query.Form1.form1.errortext.Invoke(new Action(() =>
                               {
                                   fofa_query.Form1.form1.errortext.Text = "捕获异常：无异常";
                               }));
                           }
                           string content = await result.Content.ReadAsStringAsync();
                         //  Debug.Print(content);
                           HtmlAgilityPack.HtmlDocument html = new HtmlAgilityPack.HtmlDocument();
                           html.LoadHtml(content);
                           HtmlNode layout = html.DocumentNode.SelectSingleNode("//*[@id='__layout']");
                           HtmlNodeCollection titlelist = layout.SelectNodes("//div[@class=\"contentMain\"]/div[1]/p[1]");
                           if (titlelist == null)
                           {
                               Debug.Print("titlelist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           HtmlNodeCollection iplist = layout.SelectNodes("//div[@class=\"contentMain\"]/div[@class]/p[2]/a");
                           if (iplist == null)
                           {
                               Debug.Print("iplist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           HtmlNodeCollection urllist = layout.SelectNodes("//span[@class=\"aSpan\"]/a[1]");
                           if (urllist == null)
                           {
                               Debug.Print("urllist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           HtmlNodeCollection portlist = layout.SelectNodes("//a[@class=\"portHover\"]");
                           if (portlist == null)
                           {
                               Debug.Print("prolist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           HtmlNodeCollection nationlist = layout.SelectNodes("//a[@href and @class]");
                           if (nationlist == null)
                           {
                               Debug.Print("nationlist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           HtmlNodeCollection arealist = layout.SelectNodes("//div[@class=\"contentLeft\"]/p[5]/a[1]");
                           if (arealist == null)
                           {
                               Debug.Print("arealist is null");
                               fofa_query.Form1.buttonstop(1);
                           }
                           Debug.Print(string.Format("title:{0} ip:{1} url:{2} port:{3} nation:{4}", titlelist.Count.ToString(), iplist.Count.ToString(), urllist.Count.ToString(), portlist.Count.ToString(), nationlist.Count.ToString()));
                           for (int tmpcalc = 0; tmpcalc < titlelist.Count; tmpcalc++)
                           {
                               ListViewItem item = new ListViewItem();
                               item.Text = titlelist[tmpcalc].InnerText.Replace("\n","");
                               item.SubItems.Add(urllist[tmpcalc].InnerText.Replace("\n", ""));
                               item.SubItems.Add(iplist[tmpcalc].InnerText.Replace("\n", ""));
                               item.SubItems.Add(portlist[tmpcalc].InnerText.Replace("\n", ""));
                               item.SubItems.Add(nationlist[tmpcalc].InnerText.Replace("\n", ""));
                               item.SubItems.Add(arealist[tmpcalc].InnerText.Replace("\n", ""));
                               fofa_query.Form1.form1.resultlistview.Invoke(new Action(() =>
                               {
                                   fofa_query.Form1.form1.resultlistview.Items.Add(item);
                               }));
                           }
                           fofa_query.Form1.buttonstop(1);

                       });
                    }
                    fofa_query.Form1.form1.resultlistview.Invoke(new Action(() =>
                    {
                        fofa_query.Form1.form1.savebutton.Enabled = true;
                    }));
                }
                catch(Exception error) {
                    fofa_query.Form1.form1.errortext.Invoke(new Action(() =>
                    {
                        fofa_query.Form1.form1.errortext.Text = error.Source;
                    }));
                }
            }
        }

    }
}
