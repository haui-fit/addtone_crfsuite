import re
from pprint import pprint


def split_sent(sent):
    sent = ' ' + sent + ' '
    char = ' !@#$%^&*(\'|-=[];);/.{}_,+{}:"<>?'
    start = 0
    rs = []
    for i, s in enumerate(sent):
        if s in char:
            s2 = sent[start + 1:i].strip()
            if s2:
                rs.append(s2)
            if s:
                rs.append(s)
            start = i
    return rs[1:-1]

def split_sent_postag(sent):
    sent = ' ' + sent + ' '
    char = ' !@#$%^&*(\'|-=[];);/.{},+{}:"<>?'
    start = 0
    rs = []
    for i, s in enumerate(sent):
        if s in char:
            s2 = sent[start + 1:i].strip()
            if s2:
                rs.append(s2)
            if s:
                rs.append(s)
            start = i
    return [s for s in rs[1:-1] if s.strip()]


if __name__ == '__main__':
    sent = 'Gian_lận đấu_thầu'
    # sent = 'Quỹ đạo cuối cùng của Cassini trong 5 tháng tới sẽ đưa nó tới gần sao Thổ. Tàu thăm dò sẽ nghiên cứu, khám phá nguồn gốc vành đai sao Thổ và các yếu tố trên hành tinh này. Nhằm bảo vệ Cassini trong quá trình đi qua vành đai, một ăng ten lớn sẽ được sử dụng như tấm khiên, che chắn phần còn lại của tàu. Điều này cũng giúp các nhà nghiên cứu xác định sự an toàn, trước khi đưa thêm thiết bị khoa học tới môi trường này trong tương lai.'
    print(list(split_sent_postag(sent)))
