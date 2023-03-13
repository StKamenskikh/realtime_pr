from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArgAckEvent(_message.Message):
    __slots__ = ["assetId", "event"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    event: EventVal
    def __init__(self, assetId: _Optional[int] = ..., event: _Optional[_Union[EventVal, _Mapping]] = ...) -> None: ...

class ArgAsset(_message.Message):
    __slots__ = ["assetId"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    def __init__(self, assetId: _Optional[int] = ...) -> None: ...

class ArgData(_message.Message):
    __slots__ = ["assetId", "tagsId", "timeStampFrom"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    TAGSID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFROM_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    tagsId: _containers.RepeatedScalarFieldContainer[int]
    timeStampFrom: int
    def __init__(self, assetId: _Optional[int] = ..., tagsId: _Optional[_Iterable[int]] = ..., timeStampFrom: _Optional[int] = ...) -> None: ...

class ArgDataHist(_message.Message):
    __slots__ = ["accessToken", "assetId", "tagsId", "timeStampFrom", "timeStampTo"]
    ACCESSTOKEN_FIELD_NUMBER: _ClassVar[int]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    TAGSID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFROM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPTO_FIELD_NUMBER: _ClassVar[int]
    accessToken: str
    assetId: int
    tagsId: _containers.RepeatedScalarFieldContainer[int]
    timeStampFrom: int
    timeStampTo: int
    def __init__(self, assetId: _Optional[int] = ..., tagsId: _Optional[_Iterable[int]] = ..., timeStampFrom: _Optional[int] = ..., timeStampTo: _Optional[int] = ..., accessToken: _Optional[str] = ...) -> None: ...

class ArgDataSnapShot(_message.Message):
    __slots__ = ["assetId", "tagsId"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    TAGSID_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    tagsId: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, assetId: _Optional[int] = ..., tagsId: _Optional[_Iterable[int]] = ...) -> None: ...

class ArgEvents(_message.Message):
    __slots__ = ["assetId", "timeStampFrom"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFROM_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    timeStampFrom: int
    def __init__(self, assetId: _Optional[int] = ..., timeStampFrom: _Optional[int] = ...) -> None: ...

class ArgProject(_message.Message):
    __slots__ = ["accessToken"]
    ACCESSTOKEN_FIELD_NUMBER: _ClassVar[int]
    accessToken: str
    def __init__(self, accessToken: _Optional[str] = ...) -> None: ...

class ArgSliceDataHist(_message.Message):
    __slots__ = ["accessToken", "assetId", "slicesCount", "tagsId", "timeStampFrom", "timeStampTo"]
    ACCESSTOKEN_FIELD_NUMBER: _ClassVar[int]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    SLICESCOUNT_FIELD_NUMBER: _ClassVar[int]
    TAGSID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFROM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPTO_FIELD_NUMBER: _ClassVar[int]
    accessToken: str
    assetId: int
    slicesCount: int
    tagsId: _containers.RepeatedScalarFieldContainer[int]
    timeStampFrom: int
    timeStampTo: int
    def __init__(self, assetId: _Optional[int] = ..., tagsId: _Optional[_Iterable[int]] = ..., timeStampFrom: _Optional[int] = ..., timeStampTo: _Optional[int] = ..., slicesCount: _Optional[int] = ..., accessToken: _Optional[str] = ...) -> None: ...

class ArgTags(_message.Message):
    __slots__ = ["assetId"]
    ASSETID_FIELD_NUMBER: _ClassVar[int]
    assetId: int
    def __init__(self, assetId: _Optional[int] = ...) -> None: ...

class ArgUserCredentials(_message.Message):
    __slots__ = ["isAnonymousUser", "login", "password"]
    ISANONYMOUSUSER_FIELD_NUMBER: _ClassVar[int]
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    isAnonymousUser: bool
    login: str
    password: str
    def __init__(self, login: _Optional[str] = ..., password: _Optional[str] = ..., isAnonymousUser: bool = ...) -> None: ...

class AssetHistInfo(_message.Message):
    __slots__ = ["additional", "database", "host", "password", "port", "scheme", "server", "user"]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    additional: str
    database: str
    host: str
    password: str
    port: str
    scheme: str
    server: str
    user: str
    def __init__(self, server: _Optional[str] = ..., host: _Optional[str] = ..., port: _Optional[str] = ..., database: _Optional[str] = ..., scheme: _Optional[str] = ..., user: _Optional[str] = ..., password: _Optional[str] = ..., additional: _Optional[str] = ...) -> None: ...

class AssetType(_message.Message):
    __slots__ = ["desc", "id", "idGroup", "name"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    IDGROUP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    desc: str
    id: int
    idGroup: int
    name: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., idGroup: _Optional[int] = ...) -> None: ...

class Assets(_message.Message):
    __slots__ = ["assets"]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    assets: _containers.RepeatedCompositeFieldContainer[AssetType]
    def __init__(self, assets: _Optional[_Iterable[_Union[AssetType, _Mapping]]] = ...) -> None: ...

class EventVal(_message.Message):
    __slots__ = ["additional", "cat", "comments", "eventId", "history", "info", "msg", "status", "timeStamp", "trends", "type", "user"]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    CAT_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRENDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    additional: str
    cat: str
    comments: str
    eventId: int
    history: str
    info: str
    msg: str
    status: str
    timeStamp: int
    trends: str
    type: str
    user: str
    def __init__(self, timeStamp: _Optional[int] = ..., type: _Optional[str] = ..., cat: _Optional[str] = ..., status: _Optional[str] = ..., msg: _Optional[str] = ..., additional: _Optional[str] = ..., eventId: _Optional[int] = ..., info: _Optional[str] = ..., trends: _Optional[str] = ..., user: _Optional[str] = ..., comments: _Optional[str] = ..., history: _Optional[str] = ...) -> None: ...

class Events(_message.Message):
    __slots__ = ["enentsVal"]
    ENENTSVAL_FIELD_NUMBER: _ClassVar[int]
    enentsVal: _containers.RepeatedCompositeFieldContainer[EventVal]
    def __init__(self, enentsVal: _Optional[_Iterable[_Union[EventVal, _Mapping]]] = ...) -> None: ...

class GroupAssetType(_message.Message):
    __slots__ = ["desc", "id", "name", "parentID"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENTID_FIELD_NUMBER: _ClassVar[int]
    desc: str
    id: int
    name: str
    parentID: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., parentID: _Optional[int] = ...) -> None: ...

class GroupTagsType(_message.Message):
    __slots__ = ["desc", "id", "name", "parentID"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENTID_FIELD_NUMBER: _ClassVar[int]
    desc: str
    id: int
    name: str
    parentID: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., parentID: _Optional[int] = ...) -> None: ...

class GroupsAssets(_message.Message):
    __slots__ = ["groupsAssets"]
    GROUPSASSETS_FIELD_NUMBER: _ClassVar[int]
    groupsAssets: _containers.RepeatedCompositeFieldContainer[GroupAssetType]
    def __init__(self, groupsAssets: _Optional[_Iterable[_Union[GroupAssetType, _Mapping]]] = ...) -> None: ...

class GroupsTags(_message.Message):
    __slots__ = ["groupsTags"]
    GROUPSTAGS_FIELD_NUMBER: _ClassVar[int]
    groupsTags: _containers.RepeatedCompositeFieldContainer[GroupTagsType]
    def __init__(self, groupsTags: _Optional[_Iterable[_Union[GroupTagsType, _Mapping]]] = ...) -> None: ...

class ProjectInfo(_message.Message):
    __slots__ = ["database", "host", "msg", "password", "port", "projectId", "projectName", "scheme", "server", "user"]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROJECTID_FIELD_NUMBER: _ClassVar[int]
    PROJECTNAME_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    database: str
    host: str
    msg: str
    password: str
    port: str
    projectId: int
    projectName: str
    scheme: str
    server: str
    user: str
    def __init__(self, server: _Optional[str] = ..., host: _Optional[str] = ..., port: _Optional[str] = ..., database: _Optional[str] = ..., scheme: _Optional[str] = ..., user: _Optional[str] = ..., password: _Optional[str] = ..., projectId: _Optional[int] = ..., projectName: _Optional[str] = ..., msg: _Optional[str] = ...) -> None: ...

class Ret(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: bool
    def __init__(self, answer: bool = ...) -> None: ...

class RetUserParams(_message.Message):
    __slots__ = ["login", "name", "password", "post", "role", "verifyRezult"]
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    VERIFYREZULT_FIELD_NUMBER: _ClassVar[int]
    login: str
    name: str
    password: str
    post: str
    role: str
    verifyRezult: bool
    def __init__(self, verifyRezult: bool = ..., login: _Optional[str] = ..., password: _Optional[str] = ..., name: _Optional[str] = ..., post: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class TagType(_message.Message):
    __slots__ = ["desc", "hiVal", "id", "idGroup", "isSaveInDB", "lowVal", "name", "type", "unit"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    HIVAL_FIELD_NUMBER: _ClassVar[int]
    IDGROUP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ISSAVEINDB_FIELD_NUMBER: _ClassVar[int]
    LOWVAL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    desc: str
    hiVal: float
    id: int
    idGroup: int
    isSaveInDB: bool
    lowVal: float
    name: str
    type: str
    unit: str
    def __init__(self, id: _Optional[int] = ..., idGroup: _Optional[int] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., type: _Optional[str] = ..., unit: _Optional[str] = ..., lowVal: _Optional[float] = ..., hiVal: _Optional[float] = ..., isSaveInDB: bool = ...) -> None: ...

class TagVal(_message.Message):
    __slots__ = ["isGood", "tagId", "timeStamp", "value"]
    ISGOOD_FIELD_NUMBER: _ClassVar[int]
    TAGID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    isGood: bool
    tagId: int
    timeStamp: int
    value: float
    def __init__(self, tagId: _Optional[int] = ..., timeStamp: _Optional[int] = ..., value: _Optional[float] = ..., isGood: bool = ...) -> None: ...

class Tags(_message.Message):
    __slots__ = ["tags"]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[TagType]
    def __init__(self, tags: _Optional[_Iterable[_Union[TagType, _Mapping]]] = ...) -> None: ...

class TagsDataArray(_message.Message):
    __slots__ = ["tagsVal"]
    TAGSVAL_FIELD_NUMBER: _ClassVar[int]
    tagsVal: _containers.RepeatedCompositeFieldContainer[TagVal]
    def __init__(self, tagsVal: _Optional[_Iterable[_Union[TagVal, _Mapping]]] = ...) -> None: ...

class TagsDataHistArray(_message.Message):
    __slots__ = ["fin", "msg", "tagsVal"]
    FIN_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TAGSVAL_FIELD_NUMBER: _ClassVar[int]
    fin: bool
    msg: str
    tagsVal: _containers.RepeatedCompositeFieldContainer[TagVal]
    def __init__(self, tagsVal: _Optional[_Iterable[_Union[TagVal, _Mapping]]] = ..., fin: bool = ..., msg: _Optional[str] = ...) -> None: ...
