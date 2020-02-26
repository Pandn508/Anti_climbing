# Anti_climbing
爬虫小项目库--

scrapy_test 主要是scrapy框架的练习：
    zhihuuser  可以从一个user主业爬取他的信息，并且循环爬取他的粉丝列和关注列表的所有用户的信息，存入mongdb数据库
    image360   是自动下载360美图存入根目录的爬虫，可以根据关键字的网页改变爬取对象，并将图片信息存入mysql和mongdb
    
youdao_api  是绕过签名校验反爬虫的练习，破解sign，bv，ts，salt请求值来调用有道翻译
ts是当前时间的时间戳，salt是ts+randint（1，10），sign是salt和两个字符串以及输入的文字的md5编码
用了urllib和re，可以通过import调用main（）方法输入参数当成api使用
    
qidian_climb  是由requests和xpath写的自动爬取起点小说网站所有免费小说的爬虫，
可以在root目录下自动以小说名新建文件夹，并在文件夹内按章节名常见txt文件，单独存放

bilibili   主要是练习文本点触验证码，因为太单调了就结合selenium和超级鹰弄了个自动登录功能，
可以通过改变账号密码实现自动登入


