import Server
import  rocksdb

rdb = rocksdb.DB("Slave.db", rocksdb.Options(create_if_missing=True))
mdb = rocksdb.DB("Master.db", rocksdb.Options(create_if_missing=True))
snapshot = mdb.snapshot()
snapshotr=rdb.snapshot()
it = mdb.iteritems(snapshot=snapshot)
it.seek_to_first()
print(dict(it))
itr=rdb.iteritems(snapshot=snapshotr)
itr.seek_to_first()
print(dict(itr))
# prints {b'a': b'1', b'b': b'2'}
#print (mdb.get('079e63161c5343abb8f0a4a3f0ee257a'.encode('utf-8')))


#it = mdb.iterkeys()
#it.seek_to_first()
#print(list(it))

#for key in mdb.get(list(it)):
    #mdb.delete(key.encode('utf-8'))
data="received: KEY:b'4be62391f6dd43899dccd3e6a49241af' AND DATA:b'h'"
keyindex=data.find("b'")
andindex=data.find("AND DATA:b'")
key=data[keyindex+2:andindex-2]
value=data[andindex+11:-1]
print(key)
print(value)
print(data)
initprop=str(mdb.get_live_files_metadata())
res=initprop.find("'largest_seqno'")
temp=initprop[res+17:]
op=temp.find(",")
fop=temp[:op]
print(fop)
#seqno=initprop.count("largest_seqno")
#print(initprop)
#print(key)