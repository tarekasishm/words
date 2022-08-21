# WORDS API

*WORDS API* is a kind of **CRUD** for sorted words. As any other **CRUD** it allows you to create, retrieve, update and delete sorted words but you can also
find [anagrams](https://en.wikipedia.org/wiki/Anagram). You can find the **OpenAPI** doc in https://words-api.es/docs

## Getting started



## Performance

The following performance tests have been 

```json
{
    "db" : "WORDS",
    "collections" : 1,
    "views" : 0,
    "objects" : 80383,
    "avgObjSize" : 37.8726098801986,
    "dataSize" : 2.90328407287598,
    "storageSize" : 2.6875,
    "indexes" : 1,
    "indexSize" : 2.64453125,
    "totalSize" : 5.33203125,
    "scaleFactor" : 1048576.0,
    "fsUsedSize" : 115741.421875,
    "fsTotalSize" : 929227.62109375,
    "ok" : 1.0,
    "$clusterTime" : {
        "clusterTime" : Timestamp(1660720189, 139),
        "signature" : {
            "hash" : { "$binary" : "b9yGCJWoJbxzG4J+d0p0Hn/AD5M=", "$type" : "00" },
            "keyId" : NumberLong(7082739566066532360)
        }
    },
    "operationTime" : Timestamp(1660720189, 139)
}
```

