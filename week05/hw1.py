# 操作set
import redis
client = redis.Redis(host='mysqlsev1',password='hUN7e4_1')


def counter(video_id):
    result = client.sadd('video_id_counter',video_id)
    if result == 1:
        client.set(video_id,'1')
        return 1
    else:
        r=client.incr(video_id)
    return r

print(counter(1008))
print(counter(1008))
print(counter(1009))
