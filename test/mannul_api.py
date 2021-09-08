"""
用于测试mannual-api分支上手动编写的api功能
为了测试，将Django配置文件的middleware中的
django.middleware.csrf.CsrfViewMiddleware
注释掉了，避免跨域问题
"""
import requests
import json


def test_post():
    '''验证手动编写的post api'''
    url = 'http://127.0.0.1:8000/books/'
    auth = ('admin', 'admin')
    data = {
        'title': '斗罗大陆',
        'pub_date': '2015-12-12',
        'comment': '200',
        'read': '100',
        'image': ''
    }
    data = json.dumps(data)
    result = requests.post(url, data, auth=auth)
    if result.status_code == 201:
        print('资源创建成功，POST API测试成功')
        print(result.content)
    else:
        print('资源创建失败，POST API测试失败')


def test_delete():
    '''
    验证手动编写的delete api;
    View里面写的是逻辑删除，所以数据不会实际删除，只是is_delete标记变为1
    '''
    url = 'http://127.0.0.1:8000/books/6'
    auth = ('admin', 'admin')
    result = requests.delete(url, auth=auth)
    if result.status_code == 204:
        print('资源删除成功，DELETE API测试成功')
    else:
        print('资源删除失败，DELETE API测试失败')
    

def main():
    test_post()
    test_delete()
    pass


if __name__ == '__main__':
    main()
    