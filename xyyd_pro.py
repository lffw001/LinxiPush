# Author: lindaye
# Update:2023-09-26
# 小阅阅阅读
# 活动入口：https://sd8690.viptaoyou.top:10261/yunonline/v1/auth/1c3da9bd1689d78a51463138d634512f?codeurl=sd8690.viptaoyou.top:10261&codeuserid=2&time=1694212129
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量xyytoken 值{"ck":"ysm_uid的值","ts":"Wxpusher的UID"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"ck":"ysm_uid的值","ts":"Wxpusher的UID"},{"ck":"ysm_uid的值","ts":"Wxpusher的UID"}]
# 提现说明:
#   可选参数 支付宝账号zfbzh 支付宝姓名zfbxm
#   微信提现(默认):{"ck":"ysm_uid的值","ts":"Wxpusher的UID"}
#   支付宝提现:{"ck":"ysm_uid的值","ts":"Wxpusher的UID","zfbzh":"110","zfbxm":"局子"}
# 脚本使用说明:
#   1.(必须操作)扫码关注wxpusher获取UID: https://wxpusher.zjiecode.com/demo/
#   2.在1打开的网页中点击发送文本消息,查看是否收到,收到可继续
#   3.将1打开的网页中的UID或者以及操作过1的账号UID复制备用
#   4.根据提示说明填写账号变量
# 回调服务器开放说明:
#   1.仅针对授权用户开放,需配合授权软件使用
#   2.青龙变量设置LID变量名,值为授权软件的LID
# 软件版本
version = "1.2.0"
name = "小阅阅读"
linxi_token = "xyytoken"
linxi_tips = '{"ck":"ysm_uid的值","ts":"Wxpusher的UID"}'
import requests
import json
import time
import random
import re
import os
from multiprocessing import Pool
from urllib.parse import quote
# 阅读等待时间
tsleep = 40
# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
Limit = 2
# 授权设备ID(软件版本>=1.3.3)[非授权用户不填即可]
imei = os.getenv('LID')
# 小阅阅读域名(无法使用时请更换)
domain = 'http://1695643778.tyjnwf.top'
# 保持连接,重复利用
ss = requests.session()
# 检测文章列表(如有未收录可自行添加)
check_list = [
    "MzkxNTE3MzQ4MQ==","Mzg5MjM0MDEwNw==","MzUzODY4NzE2OQ==","MzkyMjE3MzYxMg==","MzkxNjMwNDIzOA==","Mzg3NzUxMjc5Mg==",
    "Mzg4NTcwODE1NA==","Mzk0ODIxODE4OQ==","Mzg2NjUyMjI1NA==","MzIzMDczODg4Mw==","Mzg5ODUyMzYzMQ==","MzU0NzI5Mjc4OQ==",
    "Mzg5MDgxODAzMg==",
]
# 时间戳
def ts ():
    return str(int(time.time() * 1000))

# 获取个人信息模块
def user_info(i,ck):
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
        'Cookie':f"ysmuid={ck['ck']}",
        'Referer': f'{domain}/'
    }
    result = ss.get(domain,headers=headers).text
    request_id = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if request_id == []:
        print (f'账号【{i+1}】初始化失败,请检测CK({ck["ck"]})是否正确!')
        return False
    else:
        unionid = re.findall(r'unionid="(.*?)";',result)[0]
        result = ss.get(f'{domain}/yunonline/v1/sign_info?time={ts()}&unionid={unionid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False
        result = ss.get(f'{domain}/yunonline/v1/hasWechat?unionid={unionid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False
        result = ss.get(f'{domain}/yunonline/v1/gold?unionid={unionid}&time={ts()}').json()
        if result['errcode'] == 0:
            print(f"账号【{i+1}】今日积分: {result['data']['day_gold']} 已阅读: {result['data']['day_read']}篇 剩余: {result['data']['remain_read']}篇")
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False

# 阅读文章模块
def do_read(i,ck):
    time.sleep(i*5)
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
        'Cookie':f"ysmuid={ck['ck']}",
    }
    result = ss.get(domain,headers=headers).text
    request_id = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if request_id == []:
        print (f'账号【{i+1}】初始化失败,请检测CK({ck["ck"]})是否正确!')
        return False
    else:
        unionid = re.findall(r'unionid="(.*?)";',result)[0]
    if 'did' in ck:
        Did_data=f"unionid={unionid}&devid={ck['did']}"
        Did_R = ss.post( domain+'/yunonline/v1/devtouid',data=Did_data)
        print(f"账号【{i+1}】模拟上传设备指纹: {ck['did']}")
    
    result = ss.get(domain,headers=headers).text
    data = {'unionid':unionid}
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
        'Cookie':f"ysmuid={ck['ck']}; ejectCode=1",
        'Referer': 'http://1693441346.pgvv.top/',
    }
    result = ss.post(f'{domain}/yunonline/v1/wtmpdomain',json=data).json()
    uk = re.findall(r'uk=([^&]+)',result['data']['domain'])[0]
    host = re.findall(r'(http.*?)/y', result['data']['domain'])[0]
    print(f"账号【{i+1}】获取到KEY: {uk}")
    while True:
            temp_headers = {
                'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                'Origin': host,
            }
            result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}',headers=temp_headers)
            if result.text == "":
                print(f"账号【{i+1}】检测到账号已被封禁或CK错误,自动停止当前操作!")
                return False
            else:
                result = result.json()
            if result['errcode'] == 0:
                link = result['data']['link']
                link_headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                    'Cookie': f'ysmuid={ck["ck"]}; ejectCode=1'
                }
                l_result = ss.get(link,headers=link_headers).text
                # 获取biz
                biz = re.findall("biz=(.*?)&amp;",l_result)
                if biz == []:
                    print(f'账号【{i+1}】未找到BIZ,待老夫找找看')
                    pattern = r'<meta\s+property="og:url"\s+content="([^"]+)"\s*/>'
                    matches = re.search(pattern, l_result)
                    if matches:
                        fixed_url = matches.group(1)
                        og_url = fixed_url.replace("amp;", "")
                        biz = og_url.split('__biz=')[1].split('&')[0]
                    else:
                        biz = re.findall("biz=(.*?)&",link)
                        if biz == []:
                            print(f'账号【{i+1}】未找到BIZ,老夫也没找到')
                            continue
                        else:
                            biz = biz[0]
                else:
                    biz = biz[0]
                s = random.randint(6,8)
                print (f'账号【{i+1}】获取文章成功-{biz}-模拟{s}秒')
                if biz in check_list:
                    print(f"账号【{i+1}】阅读检测文章-已推送微信,请40s内完成验证!")
                    #print(f"获取到微信文章: {link}")
                    link = re.findall('_g.msg_link = "(.*?)"',l_result)[0]
                    # 过检测
                    check = check_status(ck['ts'],link,i)
                    if check == True:
                        print(f"账号【{i+1}】检测文章-过检测成功啦!")
                        r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}',headers=temp_headers).json()
                        if r_result['errcode'] == 0:
                            print(f"账号【{i+1}】阅读已完成: 获得{r_result['data']['gold']}积分 剩余{r_result['data']['remain_read']}篇")
                        elif r_result['msg'] == "本次阅读无效":
                            print(f"账号【{i+1}】检测异常重新获取:{r_result}")
                        else:
                            print(f"账号【{i+1}】检测异常:{r_result}")
                            break
                    else:
                        print(f"账号【{i+1}】检测文章-过检测失败啦!")
                        break
                else:
                    time.sleep(s)
                    r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}',headers=temp_headers).json()
                    if r_result['errcode'] == 0:
                        print(f"账号【{i+1}】阅读已完成: 获得{r_result['data']['gold']}积分 剩余{r_result['data']['remain_read']}篇")
                    else:
                        print(f"账号【{i+1}】阅读失败,获取到未收录检测BIZ:{biz}")
                        print(f"账号【{i+1}】阅读异常:{r_result}")
                        break
            else:
                if result['msg'] in ["任务重复","任务超时","阅读无效"]:
                    print(f"账号【{i+1}】阅读失败: {result['msg']}重新获取文章")
                else:
                    print (f"账号【{i+1}】阅读提醒: {result['msg']}")
                    break


# 提现模块
def get_money(i,ck):
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
        'Cookie':f"ysmuid={ck['ck']}",
        'Origin': 'http://1695525674.snak.top',
    }
    result = ss.get(domain,headers=headers).text
    request_id = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if request_id == []:
        print (f'账号【{i+1}】初始化失败,请检测CK({ck["ck"]})是否正确!')
        return False
    else:
        turl = re.findall(r'href="(.*?)">提现',result)[0]
        result = ss.get(turl,headers=headers).text
        money = re.findall(r'id="exchange_gold">(.*?)</p>',result)
        request_id = re.findall(r'request_id = "(.*?)";',result)
        unionid = re.findall(r"unionid = '(.*?)';",result)
        if money == []:
            print (f'账号【{i+1}】金币获取失败,账号异常')
        else:
            money = money[0]
            rmb = re.findall(r'money = (.*?);',result)[0]
            if int(money) >= 3000:
                tmoney = (int(money) // 3000) * 3000
                # print(f"账号【{i+1}】提交体现金币: {tmoney}")
                t_data = {'unionid':unionid,'request_id':request_id,'gold':tmoney}
                t_result = ss.post(f'{domain}/yunonline/v1/user_gold',data=t_data).json()
                # print(f'账号【{i+1}】金币转换金额{t_result}')
                money = int(money) - 3000
            if float(rmb) >= float(Limit):
                if 'zfbzh' in ck:
                    j_data = {'unionid':unionid,'signid':request_id,'ua':2,'ptype':1,'paccount':ck['zfbzh'],'pname':ck['zfbxm']}
                    j_result = ss.post(f'{domain}/yunonline/v1/withdraw',data=j_data).json()
                    print(f"账号【{i+1}】余额满足{Limit}元支付宝体现结果: {j_result['msg']}")
                else:
                    j_data = {'unionid':unionid,'signid':request_id,'ua':2,'ptype':0,'paccount':'','pname':''}
                    j_result = ss.post(f'{domain}/yunonline/v1/withdraw',data=j_data).json()
                    print(f"账号【{i+1}】余额满足{Limit}元微信体现结果: {j_result['msg']}")
            else:
                print(f"账号【{i+1}】余额小于{Limit}元暂不提现! 当前金币: {money} 当前余额:{rmb}")
           

# 微信推送模块
def check_status(key,link,index):
    if imei != None:
        if ss.get("https://linxi-send.run.goorm.io").status_code ==200:
            callback = "https://linxi-send.run.goorm.io"
        else:
            callback = "https://auth.linxi.tk"
        result = ss.post(callback+"/create_task",json={"imei":imei}).json()
        uuid = result['uuid']
        msg = result['msg']
        # print(f"账号【{str(index+1)}】避免并发,本次延迟{index*2}秒,上传服务器[{result['msg']}]")
        # time.sleep(index*2)
        # data = {
        #     "content": f"请在{tsleep}秒内完成验证!",
        #     "name": key,
        #     "project": f"检测文章-{name}",
        #     "tmpl_name": "林夕监测助手",
        #     "url": f"{quote(link)}"
        # }
        # result = requests.post(callback,json=data).json()
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-{name}%0A请在{tsleep}秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
        print(f"账号【{str(index+1)}】微信消息推送[{msg}]: {result['msg']},等待40s完成验证!")
        for i in range(10):
            result = ss.get(callback+f"/select_task/{imei}/{uuid}").json()
            if result['code'] == 200:
                print(f"账号【{str(index+1)}】服务器回调结果:{result['msg']}")
                result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
                print(f"账号【{str(index+1)}】查询本次uuid结果:{result['msg']}")
                return True
            time.sleep(tsleep/10)
        result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
        print(f"账号【{str(index+1)}】清除本次uuid结果:{result['msg']}")
        return False
    else:
        # print(f"账号【{str(index+1)}】避免并发同一时间多个推送,本次推送延迟{index*2}秒")
        # time.sleep(index*2)
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-{name}%0A请在{tsleep}秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
        print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
        #print(f"手动微信阅读链接: {link}")
        time.sleep(tsleep)
        return True

if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗██╗   ██╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝  ╚████╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗   ╚██╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗   ██║      ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═════╝ 
    项目:{name}           BY-林夕          Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv(linxi_token) == None:
            print(f'青龙变量异常: 请添加{linxi_token}变量示例:{linxi_tips} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv(linxi_token).splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            # 这里填写本地变量
        ]
        if ck_token == []:
            print(f'本地变量异常: 请添加本地ck_token示例:{linxi_tips}')
    print("==================回调服务器状态=================")
    if imei:
        print(f"[回调服务器]:已启用-[授权ID:{imei}]")
    else:
        print(f"[回调服务器]:未启用-[变量ID:{imei}]")
    # 创建进程池
    with Pool() as pool:
        # 并发执行函数
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))
        print("==================开始阅读文章=================")
        pool.starmap(do_read, list(enumerate(ck_token)))
        print("==================开始账号提现=================")
        pool.starmap(get_money, list(enumerate(ck_token)))


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
