参考链接：[【C#】标签页](https://blog.csdn.net/yongh701/article/details/50424234)

控件名称：tabControl

UI大体如下：
![l9kKxS.png](https://s2.ax1x.com/2019/12/23/l9kKxS.png)


用到的控件：
1个tabControl控件
2个 button控件
1个textbox控件
1个Group控件

学习到的知识点：
object类型 - 接收所有函数
textbox.AppendText() - 想当于把text的内容添加到一个列表
tabControl1.SelectTab - 切换标签页
tabControl1_SelectedIndexChanged - 切换标签触发函数

代码实现如下：
```C#
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

      //定义日志函数
        public void log_out(object value) //object代表接收所有类型的内容
        { //在窗体函数块内部能定义与控件属性名字一样的玩意
            textBox1.AppendText((string)value); //想当与一个列表，不会重置Text的内容
        }
        private void button2_Click(object sender, EventArgs e)
        {
            tabControl1.SelectTab(0);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            tabControl1.SelectTab(1); //切换标签页
        }

        private void tabControl1_SelectedIndexChanged(object sender, EventArgs e) //切换标签页触发的事件
        {
            log_out("时间:" + DateTime.Now.ToString() + "切换到标签页:" + tabControl1.SelectedIndex + "\r\n");
        }

        //控件自适应大小
        private void setControls(float newx, float newy, Control cons)

        {

            //遍历窗体中的控件，重新设置控件的值

            foreach (Control con in cons.Controls)

            {

                string[] mytag = con.Tag.ToString().Split(new char[] { ':' });//获取控件的Tag属性值，并分割后存储字符串数组

                float a = Convert.ToSingle(mytag[0]) * newx;//根据窗体缩放比例确定控件的值，宽度

                con.Width = (int)a;//宽度

                a = Convert.ToSingle(mytag[1]) * newy;//高度

                con.Height = (int)(a);

                a = Convert.ToSingle(mytag[2]) * newx;//左边距离

                con.Left = (int)(a);

                a = Convert.ToSingle(mytag[3]) * newy;//上边缘距离

                con.Top = (int)(a);

                Single currentSize = Convert.ToSingle(mytag[4]) * newy;//字体大小

                con.Font = new Font(con.Font.Name, currentSize, con.Font.Style, con.Font.Unit);

                if (con.Controls.Count > 0)

                {

                    setControls(newx, newy, con);

                }

            }

        }


        private void setTag(Control cons)

        {

            //遍历窗体中的控件

            foreach (Control con in cons.Controls)

            {

                con.Tag = con.Width + ":" + con.Height + ":" + con.Left + ":" + con.Top + ":" + con.Font.Size;

                if (con.Controls.Count > 0)

                    setTag(con);

            }

        }

        void Form1_Resize(object sender, EventArgs e)

        {

            float newx = (this.Width) / X; //窗体宽度缩放比例

            float newy = this.Height / Y;//窗体高度缩放比例

            setControls(newx, newy, this);//随窗体改变控件大小

        }


        float X, Y;
        private void Form1_Load(object sender, EventArgs e)
        {
            this.Resize += new EventHandler(Form1_Resize);//窗体调整大小时引发事件

            X = this.Width;//获取窗体的宽度

            Y = this.Height;//获取窗体的高度

            setTag(this);//调用方法
        }

    }
}

```