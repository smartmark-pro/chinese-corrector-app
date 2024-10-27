import streamlit as st
import time
import requests
import json


st.title("中文文本纠错应用")

st.header('一个展示文本纠错效果的应用')


st.sidebar.header('可调整参数')
correct_option = st.sidebar.selectbox(
     '选择一种文本纠错方法',
     ('NaSGECBart', 'MuCGECBart'))

length = st.sidebar.slider('句子最大长度', 1, 128, 128)

st.markdown("#### 一些例子")
examples = []
long_text = """
在一个充满生活热闹和忙碌的城市中，有一个年轻人名叫李华。他生活在北京，这座充满着现代化建筑和繁忙街道的都市。每天，他都要穿行在拥挤的人群中，追逐着自己的梦想和生活节奏。\n\n李华从小就听祖辈讲述关于福气和努力的故事。他相信，“这洋的话，下一年的福气来到自己身上”。因此，尽管每天都很忙碌，他总是尽力保持乐观和积极。\n\n某天早晨，李华骑着自行车准备去上班。北京的交通总是非常繁忙，尤其是在早高峰时段。他经过一个交通路口，看到至少两个交警正在维持交通秩序。这些交警穿着整齐的制服，手势有序而又果断，让整个路口的车辆有条不紊地行驶着。这让李华想起了他父亲曾经告诫过他的话：“在拥挤的时间里，为了让人们遵守交通规则，至少要派两个警察或者交通管理者。”\n\n李华心中感慨万千，他想要在自己的生活中也如此积极地影响他人。他虽然只是一名普通的白领，却希望能够通过自己的努力和行动，为这座城市的安全与和谐贡献一份力量。\n\n随着时间的推移，中国的经济不断发展，北京的建设也日益繁荣。李华所在的公司也因为他的努力和创新精神而蓬勃发展。他喜欢打篮球，每周都会和朋友们一起去运动场，放松身心。他也十分重视健康，每天都保持适量的饮水量，大约喝五次左右。\n\n今天，李华觉得格外开心。他意识到，自己虽然只是一个普通人，却通过日复一日的努力，终于在生活中找到了属于自己的那份福气。他明白了祖辈们口中的那句话的含义——“这洋的话，下一年的福气来到自己身上”，并且深信不疑。\n\n在这个充满希望和机遇的时代里，李华将继续努力工作，为自己的梦想而奋斗，也希望能够在这座城市中留下自己的一份足迹，为他人带来更多的希望和正能量。\n\n这就是李华的故事，一个在现代城市中追寻梦想和福气的普通青年。
"""
examples = st.selectbox("", ["", '这洋的话，下一年的福气来到自己身上。', '在拥挤时间，为了让人们尊守交通规律，派至少两个警察或者交通管理者。', '随着中国经济突飞猛近，建造工业与日俱增']+["北京是中国的都。", "他说：”我最爱的运动是打蓝球“", "我每天大约喝5次水左右。", "今天，我非常开开心。", "长文本例子"])
label2 = "  "
st.markdown('#### 输入文本')
if examples=="长文本例子":
    input=st.text_area(label=label2, value=long_text, height=100)
elif examples:
    input=st.text_area(label=label2, value=examples, height=100)
else:
    input=st.text_area(label=label2, value="", height=100)


def get_correct_res(data):
    # 等项目合并最新内容， 会去掉该接口
    url = st.secrets.remote.get("algo_url")
    res = requests.post(url=url, data=json.dumps(data))
    try:
        if res.status_code==200:
            r = res.json()
    except Exception as e:
        st.error((data, e))
        return None
    return r


if input:
    # 调用接口， 获取返回结果
    result = get_correct_res({"method": correct_option, "length": length, "input": input, "username": "", "token": "", "requestid": ""})
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    # st.success('纠错调用成功')
else:
    result = {}

# 这里用markdown简单控制下样式， 如果有进一步需求可能需要自定义组件
batch_results = result.get("sentences", [])
# print(batch_results)
left_texts, right_texts = [], []

for sr in batch_results:
    # 分句展示格式处理
    source = sr["source"]
    target = sr["target"]
    l, r = [], []
    last_end = 0
    if sr["errors"]:
        for e in sr["errors"]:

            start = e[-1]
            l.append(source[last_end:start])

            t = e[0]
            end = start + len(t)
            l.append(f":red[{source[start:end]}]")
            last_end = end

        if last_end!=0:
            l.append(source[last_end:])
        left_texts.append("".join(l))

        last_end = 0

        for e in sr["errors"]:

            start = e[-1]
            r.append(target[last_end:start])

            t = e[1]
            end = start + len(t)
            r.append(f":green[{target[start:end]}]")
            last_end = end

        if last_end!=0:
            r.append(target[last_end:])
        right_texts.append("".join(r))
    else:
        left_texts.append(source)
        right_texts.append(target)
left, right = st.columns(2)
print(len(left_texts), len(right_texts), len(batch_results))
with left:
    # 切分后内容
    st.markdown('#### 分句展示')
    for t in left_texts:
        st.markdown(t)
with right:
    # 纠错完成内容， 展示对齐内容
    st.markdown('#### 纠错后分句展示')
    for t in right_texts:
        st.markdown(t)

st.markdown('#### 最终结果')
output = st.text_area(label=" ", value=result.get("target", ""), height=100)