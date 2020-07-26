from functools import reduce
url1='weibo.com/qasak'
url2='github.com/qasak'
url3='bilibili.com/qasak'
url4='bilibili.com/xiaoming'


urls = [url1, url2, url3,url4]
# We get all domains here
domains = map(lambda u: u.split('/')[0], urls)

def get_domain_stat(stat, domain):
    if domain not in stat:
        stat[domain] = 0
    stat[domain] += 1
    return stat

# We get the stat of domains here
domain_stat = reduce(get_domain_stat, domains, {})



# reduce intrucduction:
functools.reduce(function, iterable[, initializer])
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value