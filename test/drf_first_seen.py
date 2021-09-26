import json
import requests


class APIConnection():
    '''
    Api Connection
    '''
    def __init__(self):
        self.api_url = 'http://127.0.0.1:8000'
        self.auth = ('admin', 'admin')

    def get_specific_data(self, id):
        """
        从API获取某一本书的信息
        """
        request_url = f"{self.api_url}/books/{id}"
        response = requests.get(
            request_url,
            auth=self.auth
            )

        if response.status_code == 200:
            # data = response.json()
            print("测试查询具体书本信息API成功")
            return True
        print("测试查询具体书本信息API失败")
        return False

    def post_data(self):
        '''
        创建一本书
        '''
        data = {
            'title': '云计算安全',
            'pub_date': '2015-12-12',
            'comment': '200',
            'read': '100',
            'image': ''
            }
        # 这里不要把数据转为json格式，不然会报415错
        # data = json.dumps(data)
        url = f"{self.api_url}/books/"
        try:
            response = requests.post(
                url,
                data,
                auth=self.auth
                )

            if response.status_code == 201:
                print("测试创建书本API成功")
                return True
            else:
                print("测试创建书本API失败")
                return False
        except Exception as err:
            print(err)
            print("测试创建书本API失败")
            return False

    def get_data(self):
        '''
        查询所有的书
        '''
        url = f"{self.api_url}/books/"
        try:
            response = requests.get(url, auth=self.auth)
            data = json.loads(response.text)
            if response.status_code == 200:
                print("测试查询所有书本信息API成功")
                return True
            else:
                print("测试查询具体书本信息API失败")
                return False
        except Exception as err:
            print(err)
            print("测试查询具体书本信息API失败")
            return False

    def delete(self, id):
        '''
        删除一本具体的书
        '''
        url = f"{self.api_url}/books/{id}"

        try:
            # 这里是真实的物理删除，
            # 如果测试逻辑删除的话应该是修改is_delete这个标志位的值为True
            res = requests.delete(url, auth=self.auth)
            if res.status_code == 204:
                print("测试删除API成功")
                return True
            print("测试删除API失败")
            return False

        except Exception as err:
            print(err)
            print("测试删除API失败")
            return False

    def update_data(self, id):
        '''
        更新一本书
        '''
        data = {
            'title': '云计算安全',
            'pub_date': '2015-12-12',
            'comment': '200',
            'read': '100',
            'image': '',
            }
        url = f"{self.api_url}/books/{id}/"  # 使用PUT请求方法时一定要以反斜杠作为url的结尾，不然会报错
        try:
            res = requests.put(
                url,
                data,
                auth=self.auth
                )
            if res.status_code == 200:
                print("测试更新API成功")
                return True
            print("测试更新API失败")
            return False

        except Exception as err:
            print(err)
            print("测试更新API失败")
            return False


def main():
    conn = APIConnection()
    conn.get_specific_data(2)
    conn.post_data()
    conn.get_data()
    conn.update_data(10)
    conn.delete(10)
 

if __name__ == '__main__':
    main()
    