namespace fofa_query
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.cookiebox = new System.Windows.Forms.TextBox();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.contextMenuStrip2 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.pagebox = new System.Windows.Forms.TextBox();
            this.searchbox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.querybox = new System.Windows.Forms.Button();
            this.searchcurl = new System.Windows.Forms.TextBox();
            this.urllabel = new System.Windows.Forms.Label();
            this.title = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.url = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.ip = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.resultlistview = new System.Windows.Forms.ListView();
            this.port = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.nation = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.area = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.errortext = new System.Windows.Forms.Label();
            this.timesleep = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.savebutton = new System.Windows.Forms.Button();
            this.importbutton = new System.Windows.Forms.Button();
            this.label5 = new System.Windows.Forms.Label();
            this.savelist = new System.Windows.Forms.CheckedListBox();
            this.clearbutton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // cookiebox
            // 
            this.cookiebox.Location = new System.Drawing.Point(74, 29);
            this.cookiebox.Name = "cookiebox";
            this.cookiebox.Size = new System.Drawing.Size(348, 21);
            this.cookiebox.TabIndex = 0;
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(61, 4);
            // 
            // contextMenuStrip2
            // 
            this.contextMenuStrip2.Name = "contextMenuStrip2";
            this.contextMenuStrip2.Size = new System.Drawing.Size(61, 4);
            this.contextMenuStrip2.Opening += new System.ComponentModel.CancelEventHandler(this.contextMenuStrip2_Opening);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 38);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 12);
            this.label1.TabIndex = 3;
            this.label1.Text = "cookie";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 105);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(29, 12);
            this.label2.TabIndex = 4;
            this.label2.Text = "page";
            // 
            // pagebox
            // 
            this.pagebox.Location = new System.Drawing.Point(74, 105);
            this.pagebox.Name = "pagebox";
            this.pagebox.Size = new System.Drawing.Size(63, 21);
            this.pagebox.TabIndex = 5;
            this.pagebox.Text = "2";
            // 
            // searchbox
            // 
            this.searchbox.Location = new System.Drawing.Point(74, 56);
            this.searchbox.Name = "searchbox";
            this.searchbox.Size = new System.Drawing.Size(348, 21);
            this.searchbox.TabIndex = 6;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 65);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(41, 12);
            this.label3.TabIndex = 7;
            this.label3.Text = "search";
            // 
            // querybox
            // 
            this.querybox.Location = new System.Drawing.Point(194, 105);
            this.querybox.Name = "querybox";
            this.querybox.Size = new System.Drawing.Size(75, 23);
            this.querybox.TabIndex = 8;
            this.querybox.Text = "query";
            this.querybox.UseVisualStyleBackColor = true;
            this.querybox.Click += new System.EventHandler(this.querybox_Click);
            // 
            // searchcurl
            // 
            this.searchcurl.Location = new System.Drawing.Point(74, 2);
            this.searchcurl.Name = "searchcurl";
            this.searchcurl.Size = new System.Drawing.Size(406, 21);
            this.searchcurl.TabIndex = 10;
            this.searchcurl.Text = "https://fofa.info/result?qbase64={0}&page={1}&page_size=10";
            // 
            // urllabel
            // 
            this.urllabel.AutoSize = true;
            this.urllabel.Location = new System.Drawing.Point(12, 9);
            this.urllabel.Name = "urllabel";
            this.urllabel.Size = new System.Drawing.Size(23, 12);
            this.urllabel.TabIndex = 11;
            this.urllabel.Text = "url";
            // 
            // title
            // 
            this.title.Text = "title";
            this.title.Width = 122;
            // 
            // url
            // 
            this.url.Text = "url";
            this.url.Width = 158;
            // 
            // ip
            // 
            this.ip.Text = "ip";
            this.ip.Width = 106;
            // 
            // resultlistview
            // 
            this.resultlistview.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.title,
            this.url,
            this.ip,
            this.port,
            this.nation,
            this.area});
            this.resultlistview.FullRowSelect = true;
            this.resultlistview.GridLines = true;
            this.resultlistview.Location = new System.Drawing.Point(12, 168);
            this.resultlistview.Name = "resultlistview";
            this.resultlistview.Size = new System.Drawing.Size(638, 288);
            this.resultlistview.TabIndex = 9;
            this.resultlistview.UseCompatibleStateImageBehavior = false;
            this.resultlistview.View = System.Windows.Forms.View.Details;
            // 
            // port
            // 
            this.port.Text = "port";
            this.port.Width = 75;
            // 
            // nation
            // 
            this.nation.Text = "nation";
            this.nation.Width = 115;
            // 
            // area
            // 
            this.area.Text = "area";
            this.area.Width = 173;
            // 
            // errortext
            // 
            this.errortext.AutoSize = true;
            this.errortext.Location = new System.Drawing.Point(14, 463);
            this.errortext.Name = "errortext";
            this.errortext.Size = new System.Drawing.Size(89, 12);
            this.errortext.TabIndex = 12;
            this.errortext.Text = "异常捕获输出：";
            // 
            // timesleep
            // 
            this.timesleep.FormattingEnabled = true;
            this.timesleep.Items.AddRange(new object[] {
            "1000",
            "5000",
            "10000",
            "15000",
            "20000"});
            this.timesleep.Location = new System.Drawing.Point(596, 1);
            this.timesleep.Name = "timesleep";
            this.timesleep.Size = new System.Drawing.Size(102, 20);
            this.timesleep.TabIndex = 14;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(501, 5);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(89, 12);
            this.label4.TabIndex = 15;
            this.label4.Text = "延时设置(毫秒)";
            // 
            // savebutton
            // 
            this.savebutton.Location = new System.Drawing.Point(306, 105);
            this.savebutton.Name = "savebutton";
            this.savebutton.Size = new System.Drawing.Size(82, 23);
            this.savebutton.TabIndex = 16;
            this.savebutton.Text = "save";
            this.savebutton.UseVisualStyleBackColor = true;
            this.savebutton.Click += new System.EventHandler(this.savebutton_Click);
            // 
            // importbutton
            // 
            this.importbutton.Location = new System.Drawing.Point(405, 105);
            this.importbutton.Name = "importbutton";
            this.importbutton.Size = new System.Drawing.Size(75, 23);
            this.importbutton.TabIndex = 17;
            this.importbutton.Text = "import";
            this.importbutton.UseVisualStyleBackColor = true;
            this.importbutton.Click += new System.EventHandler(this.importbutton_Click);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(501, 38);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(53, 12);
            this.label5.TabIndex = 18;
            this.label5.Text = "保存选项";
            // 
            // savelist
            // 
            this.savelist.FormattingEnabled = true;
            this.savelist.Items.AddRange(new object[] {
            "title",
            "url",
            "ip",
            "port",
            "nation",
            "area"});
            this.savelist.Location = new System.Drawing.Point(596, 38);
            this.savelist.Name = "savelist";
            this.savelist.Size = new System.Drawing.Size(90, 100);
            this.savelist.TabIndex = 19;
            // 
            // clearbutton
            // 
            this.clearbutton.Location = new System.Drawing.Point(503, 105);
            this.clearbutton.Name = "clearbutton";
            this.clearbutton.Size = new System.Drawing.Size(78, 23);
            this.clearbutton.TabIndex = 20;
            this.clearbutton.Text = "clear";
            this.clearbutton.UseVisualStyleBackColor = true;
            this.clearbutton.Click += new System.EventHandler(this.clearbutton_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(767, 488);
            this.Controls.Add(this.clearbutton);
            this.Controls.Add(this.savelist);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.importbutton);
            this.Controls.Add(this.savebutton);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.timesleep);
            this.Controls.Add(this.errortext);
            this.Controls.Add(this.urllabel);
            this.Controls.Add(this.searchcurl);
            this.Controls.Add(this.resultlistview);
            this.Controls.Add(this.querybox);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.searchbox);
            this.Controls.Add(this.pagebox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.cookiebox);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox cookiebox;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox pagebox;
        private System.Windows.Forms.TextBox searchbox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button querybox;
        private System.Windows.Forms.TextBox searchcurl;
        private System.Windows.Forms.Label urllabel;
        private System.Windows.Forms.ColumnHeader title;
        private System.Windows.Forms.ColumnHeader url;
        private System.Windows.Forms.ColumnHeader ip;
        private System.Windows.Forms.ListView resultlistview;
        private System.Windows.Forms.ColumnHeader port;
        private System.Windows.Forms.ColumnHeader nation;
        private System.Windows.Forms.ColumnHeader area;
        private System.Windows.Forms.Label errortext;
        private System.Windows.Forms.ComboBox timesleep;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button savebutton;
        private System.Windows.Forms.Button importbutton;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.CheckedListBox savelist;
        private System.Windows.Forms.Button clearbutton;
    }
}

