import feedparser
import listparser
from pathlib import Path
import datetime
import shutil
# 获取当前日期作为文件夹名称
today = datetime.datetime.now().strftime("%Y-%m-%d")
root_path = Path(__file__).absolute().parent

# 创建以日期命名的文件夹路径
date_folder_path = root_path.joinpath(f"rss/{today}")
date_folder_path.mkdir(parents=True, exist_ok=True)
rss_path = root_path.joinpath("rss")
rss_path.mkdir(exist_ok=True)

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

seccollecter_banner = f"""
SecCollecter is a program that collects and aggregates daily security advice{yellow}
 $$$$$$\                       $$$$$$\            $$\ $$\                       $$\                         {green}
$$  __$$\                     $$  __$$\           $$ |$$ |                      $$ |                        {blue}
$$ /  \__| $$$$$$\   $$$$$$$\ $$ /  \__| $$$$$$\  $$ |$$ | $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  {red}
\$$$$$$\  $$  __$$\ $$  _____|$$ |      $$  __$$\ $$ |$$ |$$  __$$\ $$  _____|\_$$  _|  $$  __$$\ $$  __$$\ {green}
 \____$$\ $$$$$$$$ |$$ /      $$ |      $$ /  $$ |$$ |$$ |$$$$$$$$ |$$ /        $$ |    $$$$$$$$ |$$ |  \__|{blue}
$$\   $$ |$$   ____|$$ |      $$ |  $$\ $$ |  $$ |$$ |$$ |$$   ____|$$ |        $$ |$$\ $$   ____|$$ |      {yellow}
\$$$$$$  |\$$$$$$$\ \$$$$$$$\ \$$$$$$  |\$$$$$$  |$$ |$$ |\$$$$$$$\ \$$$$$$$\   \$$$$  |\$$$$$$$\ $$ |      {blue}
 \______/  \_______| \_______| \______/  \______/ \__|\__| \_______| \_______|   \____/  \_______|\__|      {green}

 program is running...                                                                                                        
"""


# 导入OPML文件
def import_opml(opml_file):
    with open(opml_file, 'r', encoding='utf-8') as file:
        data = file.read()
    return listparser.parse(data).feeds

def copy_css_files(css_file_names, destination):
    for css_file_name in css_file_names:
        source_path = root_path.joinpath(css_file_name)
        destination_path = destination.joinpath(css_file_name)
        if source_path.exists():
            shutil.copy(source_path, destination_path)
        else:
            print(f"CSS file not found: {source_path}")

# 获取RSS订阅内容
def fetch_feed(feed_url):
    return feedparser.parse(feed_url)


def entry_to_html(entry):
    title = entry.get('title', ' ')
    description = entry.get('description', ' ')
    link = entry.get('link', '#')
    return f"""
    <li>
						<h3>{title}</h3>
						<p>{description}</p>
						<a href='{link}'>Read More</a><hr>
	</li>
	"""


def feed_to_html(feed):
    feed_title = feed.feed.get('title', 'Unnamed Feed')
    entries_html = "".join(entry_to_html(entry) for entry in feed.entries)
    return f"<div class='section'>\n<h1>{feed_title}</h1>\n{entries_html}</div>\n"


def write_feed_to_html(feed, html_file_path):
    feed_title = feed.feed.get('title', 'Unnamed Feed').replace(':', '-').replace('/', '-')  # 替换标题中的不合法字符
    entries_html = "".join(entry_to_html(entry) for entry in feed.entries)
    html_content = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title></title>
	<meta name="keywords" content="" />
	<meta name="description" content="" />
	<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
	<link href="default.css" rel="stylesheet" type="text/css" media="all" />
	<link href="fonts.css" rel="stylesheet" type="text/css" media="all" />

	<!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

</head>

<body>
	<div id="page" class="container">
		<div id="header">
			<div id="logo">
				<img src=" " alt="" />
				<h1><a href="#">SecCollection</a></h1><br>
				<h1><a href="#">每日安全资讯汇总</a></h1>
			</div>
			<div id="menu">
				<ul>
					<li><a href="index.html" accesskey="1" title="">汇总</a></li>
					<li><a href="CNVD漏洞平台.html" accesskey="3" title="">CNVD漏洞平台</a></li>
					<li><a href="FreeBuf网络安全行业门户.html" accesskey="4" title="">FreeBuf</a></li>
					<li><a href="paper - Last paper.html" accesskey="5" title="">Paper</a></li>
					<li><a href="安全客-有思想的安全新媒体.html" accesskey="2" title="">安全客</a></li>
					<li><a href="绿盟科技技术博客.html" accesskey="3" title="">绿盟</a></li>
					<li><a href="奇安信 CERT.html" accesskey="4" title="">奇安信CERT</a></li>
					<li><a href="腾讯玄武实验室.html" accesskey="5" title="">腾讯玄武实验室</a></li>
				</ul>
			</div>
		</div>
		<div id="main">
			<div id="featured">
				<div class="title">
					<h2>{feed_title}</h2>
					<span class="byline">Sec</span>
				</div>
				<ul class="style1">
					{entries_html}
				</ul>
			</div>
		</div>
	</div>

</body>

</html>
"""
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


def create_index_html(summaries, index_file_path):
    index_content = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>每日安全资讯</title>
	<meta name="keywords" content="" />
	<meta name="description" content="" />
	<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
	<link href="default.css" rel="stylesheet" type="text/css" media="all" />
	<link href="fonts.css" rel="stylesheet" type="text/css" media="all" />

	<!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

</head>

<body>
	<div id="page" class="container">
		<div id="header">
			<div id="logo">
				<img src=" " alt="" />
				<h1><a href="#">SecCollection</a></h1><br>
				<h1><a href="#">每日安全资讯汇总</a></h1>
			</div>
			<div id="menu">
				<ul>
					<li class="current_page_item"><a href="index.html" accesskey="1" title="">汇总</a></li>
					<li><a href="CNVD漏洞平台.html" accesskey="3" title="">CNVD漏洞平台</a></li>
					<li><a href="FreeBuf网络安全行业门户.html" accesskey="4" title="">FreeBuf</a></li>
					<li><a href="paper - Last paper.html" accesskey="5" title="">Paper</a></li>
					<li><a href="安全客-有思想的安全新媒体.html" accesskey="2" title="">安全客</a></li>
					<li><a href="绿盟科技技术博客.html" accesskey="3" title="">绿盟</a></li>
					<li><a href="奇安信 CERT.html" accesskey="4" title="">奇安信CERT</a></li>
					<li><a href="腾讯玄武实验室.html" accesskey="5" title="">腾讯玄武实验室</a></li>
				</ul>
			</div>
		</div>
		<div id="main">
			<div id="featured">
				<div class="title">
					<h2>资讯汇总</h2>
					<span class="byline">Sec</span>
				</div>
				<ul class="style1">"""
    mains_title = summaries[0]['feed_title']
    index_content += f"<li><h3>{mains_title}</h3>"
    for summary in summaries:
        main_title=summary['feed_title']
        if main_title != mains_title:
            mains_title=main_title
            index_content += f"</li><li><h3>{mains_title}</h3>"
        index_content += f"<p>- {summary['entry_title']}</p>\n"
    index_content += f"""					</li>
				</ul>
			</div>
		</div>
	</div>
	
</body>

</html>"""

    with open(index_file_path, 'w', encoding='utf-8') as file:
        file.write(index_content)


# 程序主体部分
def main():
    print(seccollecter_banner)
    opml_file = root_path.joinpath('feed.opml')  # 假设OPML文件位于与脚本同一目录下
    feeds_data = import_opml(opml_file)

    feed_summaries = []
    css_files_to_copy = ['default.css', 'fonts.css']
    copy_css_files(css_files_to_copy, date_folder_path)
    for feed_data in feeds_data:
        feed = fetch_feed(feed_data['url'])
        feed_title = feed.feed.get('title', 'Unnamed Feed').replace(':', '-').replace('/', '-')  # 安全文件名
        html_filename = date_folder_path.joinpath(f"{feed_title}.html")
        write_feed_to_html(feed, html_filename)
        print(f"HTML file created at: {html_filename}")
        for entry in feed.entries:
            feed_summaries.append({
                'feed_title': feed_title,
                'entry_title': entry.get('title', ' '),
                'file_path': f"./{today}/{feed_title}.html"
            })

    index_file_path = date_folder_path.joinpath('index.html')
    create_index_html(feed_summaries, index_file_path)
    print(f"Index file created at: {index_file_path}")



if __name__ == '__main__':
    main()