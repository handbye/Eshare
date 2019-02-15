from django.shortcuts import render
import markdown2,os

def mdtoHtml(request,name):
    path = "./docs"
    files = os.listdir(path)
    for file in files:
        file_ex = os.path.splitext(file)[1]
        if file_ex == ".md":
            with open('./docs/'+name+'.md','r',encoding='utf8') as md:
                content = md.read()
                html = '''
<html lang="zh-cn">
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
<link href="./code.css" rel="stylesheet">
</head>
<body>
<div class="cnblogs-markdown">
%s
</div>
</body>
</html>
                '''
                ret = markdown2.markdown(content,extras=["code-friendly","code-color","fenced-code-blocks"])
                html_content = html % ret
    return render(request,'docs/doc.html',locals())