from __future__ import print_function
import logging
import grpc

from . import GRPCProto_pb2
from . import GRPCProto_pb2_grpc
from datetime import datetime,timedelta
import psycopg2
from psycopg2 import sql
import asyncio
from grpc import aio
import xml.etree.ElementTree as ET
import traceback

class ClientGrpc:

    def __init__(self):
        # СОЗДАНИЕ КАНАЛА
        f = open('config.txt', 'r')
        config = f.readline().split(',')
        f.close()
        host = config[0]
        port = config[1]
        self.channel = grpc.insecure_channel(host + ':' + port)
        self.stub = GRPCProto_pb2_grpc.GRPCProtoStub(self.channel)


    @staticmethod
    def InitializeChannel():
        global channel,stub
        f = open('config.txt', 'r')
        config = f.readline().split(',')
        f.close()
        host = config[0]
        port = config[1]
        channel = grpc.insecure_channel(host + ':' + port,[("grpc.max_receive_message_length", 32 * 1024 * 1024)])
        stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)

    @staticmethod
    def Connect(host,port,exceptStr):
        global channel,stub
        try:
            channel = grpc.insecure_channel(host + ':' + port,[("grpc.max_receive_message_length", 32 * 1024 * 1024)])
            stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)
            conectRet = stub.Connect(GRPCProto_pb2.Ret())
            if conectRet.answer:
                #self.Stopwatch.stop()
                #self.Stopwatch.reset()
                return True
            else:
                #self.Stopwatch.stop()
                #self.Stopwatch.reset()
                return False

        except Exception as e:
            if e == grpc.RpcError:
                exceptStr = e.StatusCode
                print(exceptStr)
            else:
                exceptStr = e
                print(e)
            return False


    def Disconnect(self,exceptStr):
        try:
            if self.channel != None:
                self.channel.close()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


    def StateConnect(self):
        print('checking state')
        self.channel.subscribe(on_connectivity_change,try_to_connect=True)

        return self.channel.unsubscribe(on_connectivity_change)

    @staticmethod
    def GetProjectInfo():
        global stub,channel
        try:
            readProjectInfo = stub.GetProjectInfo(GRPCProto_pb2.ArgProject(accessToken=''))
            ProjectInfo = {'server':readProjectInfo.server, 'host':readProjectInfo.host,
                            'port':readProjectInfo.port, 'database':readProjectInfo.database,
                            'scheme':readProjectInfo.scheme,'user':readProjectInfo.user,
                            'password':readProjectInfo.password, 'projectId':readProjectInfo.projectId,
                            'projectName':readProjectInfo.projectName,'msg':readProjectInfo.msg}
            return ProjectInfo
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def GetAssets(self):
        global stub,channel
        try:
            readAssets = stub.GetAssets(GRPCProto_pb2.Ret())
            Assets = []
            for item in readAssets.assets:
                Assets.append({'Id': item.id, 'Name': item.name,
                               'Desc': item.desc, 'idGroup': item.idGroup})
            return Assets
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def GetAssetGroups(assetId):
        global stub,channel
        try:
            readAssetGroups = stub.GetGroupsAsset(GRPCProto_pb2.ArgAsset(assetId=assetId))
            AssetGroups = []
            for item in readAssetGroups.groupsAssets:
                AssetGroups.append({'id':item.id,'Name':item.name,
                               'Desc':item.desc,'parentId':item.parentID})
            return AssetGroups
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def GetAssetsFromPostgreSQL(projectInfo):
        try:
            conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                    password=projectInfo['password'], host=projectInfo['host'],
                                    port=projectInfo['port'])
            cursor = conn.cursor()
            sqll = """
                        SELECT "ID","GroupID","Changes","Name","Desc","SchemaName","Config"
                        FROM {}."Assets"
                   """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets')))
            data = cursor.fetchall()
            Assets = []
            for item in data:
                Assets.append({'Id':item[0],'GroupId':item[1],
                                    'Changes':item[2],'Name':item[3],
                                    'Desc':item[4],'SchemaName':item[5],
                                    'Config':item[6]})
            return Assets
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def GetAssetGroupsFromPostgreSQL(projectInfo):
        try:
            conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                    password=projectInfo['password'], host=projectInfo['host'],
                                    port=projectInfo['port'])
            cursor = conn.cursor()
            sqll = """
                        SELECT "ID","ParentID","Changes","Name","Desc"
                        FROM {}."AssetGroups"
                   """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets')))
            data = cursor.fetchall()
            AssetGroups = []
            for item in data:
                AssetGroups.append({'Id':item[0],'ParentId':item[1],
                                    'Changes':item[2],'Name':item[3],
                                    'Desc':item[4]})
            return AssetGroups
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def GetAssetHistInfo(assetId):
        global stub,channel
        try:
            readInfo = stub.GetAssetHistInfo(GRPCProto_pb2.ArgAsset(assetId=assetId))
            assetHistInfo = {'server':readInfo.server, 'host':readInfo.host,
                             'port':readInfo.port, 'database':readInfo.database,
                             'scheme':str(readInfo.scheme),'user':readInfo.user,
                             'additional':readInfo.additional,'pass': readInfo.password}
            return assetHistInfo
        except grpc.RpcError as err:
            print(str(err))
            return False

    @staticmethod
    def GetAssetHistLastDateTime(assetHistInfo):
        lastDateTime = datetime.now()
        if assetHistInfo['server'] in ['pgsql','PgSql']:
            return ClientGrpc.GetAssetHistLastDateTimeFromPostgreSQL(assetHistInfo)
        else:
            print("dataBaseTypeNotFound")
            return False

    @staticmethod
    def GetAssetHistLastDateTimeFromPostgreSQL(assetHistInfo):
        try:
            conn = psycopg2.connect(database=assetHistInfo['database'], user=assetHistInfo['user'],
                                    password=assetHistInfo['pass'], host=assetHistInfo['host'],
                                    port=assetHistInfo['port'])
            cursor = conn.cursor()
            #sqll = """
            #SELECT MAX("DateTime") FROM {}."Data"
            #"""
            sqll = """
            SELECT "DateTime" FROM {}."SlicesDT" ORDER BY "DateTime" DESC LIMIT 1
            """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])))
            StrMaxVal = cursor.fetchall()
            lastDateTime = datetime(StrMaxVal[0][0].year, StrMaxVal[0][0].month,
                                     StrMaxVal[0][0].day, StrMaxVal[0][0].hour,
                                     StrMaxVal[0][0].minute, StrMaxVal[0][0].second, )
            return StrMaxVal[0][0]

        except Exception as e:
            print(e)
            return False

        finally:
            if conn:
                cursor.close()
                conn.close()


    @staticmethod
    def GetAssetHistFirstDateTime(assetHistInfo):
        if assetHistInfo['server'] not in ['pgsql','PgSql']:
            print('no pgsql')
            return False

        try:
            conn = psycopg2.connect(database=assetHistInfo['database'], user=assetHistInfo['user'],
                                    password=assetHistInfo['pass'], host=assetHistInfo['host'],
                                    port=assetHistInfo['port'])
            cursor = conn.cursor()
            sqll = """
                   SELECT "DateTime" FROM {}."SlicesDT" ORDER BY "DateTime" LIMIT 1
                   """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])))
            StrMinVal = cursor.fetchall()
            #firstDateTime = datetime(StrMinVal[0][0].year,StrMinVal[0][0].month,
            #                         StrMinVal[0][0].day,StrMinVal[0][0].hour,
            #                         StrMinVal[0][0].minute,StrMinVal[0][0].second,)
            return StrMinVal[0][0]

        except Exception as e:
            print(e)
            return False

        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def GetHistEvents(assetHistInfo,dateTimeFrom,dateTimeTo):

        if assetHistInfo['server'] not in ['pgsql','PgSql']:
            print('no pgsql')
            return False

        #try:
        events = []
        #print(assetHistInfo)
        conn = psycopg2.connect(database=assetHistInfo['database'], user=assetHistInfo['user'],
                                password=assetHistInfo['pass'], host=assetHistInfo['host'],
                                port=assetHistInfo['port'])
        cursor = conn.cursor()
        sqll = """
            SELECT "DateTime","Type","Category","Status","Message","Additional",
            "ID","Info","Trends","User","Comments","History"
            FROM {}."Events"
            WHERE "DateTime" >= %s AND "DateTime" < %s ORDER BY "DateTime"
        """
        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])),
            [dateTimeFrom, dateTimeTo])
        res = cursor.fetchall()
        #print(res)

        for item in res:
            events.append({'TimeStamp': item[0], 'Msg': item[4],
                           'Type': item[1], 'Cat': item[2], 'Status': item[3],
                           'Additional': item[5], 'EventId': item[6], 'Info': item[7],
                           'Trends': item[8], 'User': item[9], 'Comments': item[10],
                           'History': item[11]
                           })
        return events

        #except Exception as e:
        #    print(e)
        #    return False

        #finally:
        #    if conn:
         #       cursor.close()
        #        conn.close()

    @staticmethod
    def GetHistData(assetId,assetHistInfo,dateTimeFrom,dateTimeTo,idTags):
        if assetHistInfo['server'] in ['pgsql','PgSql']:
            return ClientGrpc.GetHistDataFromPGSQL(assetHistInfo,dateTimeFrom,dateTimeTo,idTags)
        else:
            print("dataBaseTypeNotFound")
            return False

    @staticmethod
    def GetHistDataFromPGSQL(assetHistInfo,dateTimeFrom,dateTimeTo,idTags):
        if assetHistInfo['server'] not in ['pgsql','PgSql']:
            print('no pgsql')
            return False

        try:
            conn = psycopg2.connect(database=assetHistInfo['database'], user=assetHistInfo['user'],
                                    password=assetHistInfo['pass'], host=assetHistInfo['host'],
                                    port=assetHistInfo['port'])
            cursor = conn.cursor()

            result = []
            for item in idTags:
                sqll = """ 
                SELECT "DateTime", "Val"  FROM {}."Data_""" + str(item) + """" 
                WHERE "DateTime" >= %s AND "DateTime" < %s ORDER BY "DateTime"
                """
                cursor.execute(
                    sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])),
                    [dateTimeFrom, dateTimeTo])
                res = cursor.fetchall()
                result.extend(res)
            return result

        except Exception as e:
            print(e)
            return False

        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def GetSliceHistData(assetId,assetHistInfo,dateTimeFrom,dateTimeTo,idTags,countRange,disPeriod):
        if assetHistInfo['server'] in ['pgsql','PgSql']:
            return ClientGrpc.GetSliceHistDataFromPGSQL(assetHistInfo,dateTimeFrom,dateTimeTo,idTags,countRange,disPeriod)
        else:
            print("dataBaseTypeNotFound")
            return False

    @staticmethod
    def GetSliceHistDataFromPGSQL(assetHistInfo,dateTimeFrom,dateTimeTo,idTags,countRange,disPeriod):
        if assetHistInfo['server'] not in ['pgsql','PgSql']:
            print('no pgsql')
            return False

        #try:
        conn = psycopg2.connect(database=assetHistInfo['database'], user=assetHistInfo['user'],
                                password=assetHistInfo['pass'], host=assetHistInfo['host'],
                                port=assetHistInfo['port'])
        cursor = conn.cursor()
        sqll = """
                    SELECT "DateTime" FROM {}."SlicesDT" ORDER BY "DateTime" DESC LIMIT 1
                    """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])))
        AssetLastDateTime = cursor.fetchall()[0][0]
        sqll = """
                    SELECT "DateTime" FROM {}."SlicesDT" ORDER BY "DateTime" LIMIT 1
                    """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])))
        AssetFirstDateTime = cursor.fetchall()[0][0]
        #формирование колонок для чтения
        columns = ","
        for item in idTags:
            columns = columns + """"Val_""" + str(item) + """","IsGood_""" + str(item) + """","""
        columns = columns.rstrip(',')
        #вычисление периода среза
        slicePerSec = (dateTimeTo - dateTimeFrom).total_seconds() / countRange
        if slicePerSec <= 0:
            print('интервал времени задан неверно')
            return False
        res = []
        for item in idTags:
            sliceTimeStamp = dateTimeFrom #метка времени для циклического чтения срезов
            for i in range(0,countRange):
                StrBeginTimeStamp = sliceTimeStamp
                StrEndTimeStamp = sliceTimeStamp + timedelta(seconds=slicePerSec)
                sliceTimeStamp = StrEndTimeStamp


                sqll = """ 
                SELECT "DateTime","Val" FROM {}."Data_""" + str(item) + """" 
                    WHERE "DateTime" >= %s AND "DateTime" < %s ORDER BY "DateTime" DESC LIMIT 1
                    """
                cursor.execute(
                    sql.SQL(sqll).format(sql.Identifier(assetHistInfo['scheme'])),
                    [StrBeginTimeStamp, StrEndTimeStamp])
                res.extend(cursor.fetchall())

        return res

        #except Exception as e:
        #    print(e)
        #    return False

        #finally:
        if conn:
            cursor.close()
            conn.close()

    @staticmethod
    def GetTagGroups(assetId):
        global channel,stub
        groupsTag = []
        #try:
        readGroupsTags = stub.GetGroupsTags(GRPCProto_pb2.ArgTags(assetId=assetId))
        for item in readGroupsTags.groupsTags:
            groupsTag.append({'Id': item.id, 'Name': item.name, 'Desc': item.desc, 'parentID': item.parentID})
        return groupsTag
        #except Exception as e:
        #    print(e)
        #    return False

    @staticmethod
    def GetTags(assetId):
        global channel,stub
        Tags = []
        try:
            readTags = stub.GetTags(GRPCProto_pb2.ArgTags(assetId=assetId))
            for item in readTags.tags:
                Tags.append({'Id':item.id,'IdGroup':item.idGroup,'Name':item.name,
                             'Desc':item.desc,'Type':item.type,'Unit':item.unit,
                             'HiVal':item.hiVal,'LowVal':item.lowVal,'isSaveInDB':item.isSaveInDB})
            return Tags
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def GetDataSnapShot(assetId,tagsId):
        global stub,channel
        data = []
        try:
            arg = GRPCProto_pb2.ArgDataSnapShot(assetId=assetId,
                                                tagsId=tagsId[:])
            readdata = stub.GetDataSnapShot(arg)

            #for item in readdata:
            for item in readdata.tagsVal:
                data.append({'tagId':item.tagId,'TimeStamp':item.timeStamp,'Value':item.value,
                            'IsGood':item.isGood})
            return data
        except Exception as e:
            with open('log.txt', 'a') as f:
              f.write(datetime.now().strftime('%m-%d-%Y %H:%M:%S')+' '+str(e)+'\n'+str(traceback.format_exc())+'\n')

            return False

    @staticmethod
    def GetData(assetId,tagsId,timeStampFrom):
        global channel,stub
        data= []
        try:
            arg = GRPCProto_pb2.ArgData(assetId=assetId,
                                        tagsId=tagsId[:],
                                        timeStampFrom=timeStampFrom)
            readdata = stub.GetData(arg)
            for item in readdata.tagsVal:
                data.append({'tagId':item.tagId,'TimeStamp':item.timeStamp,'Value':item.value,
                             'IsGood':item.isGood})

            return data
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def GetEvents(assetId,timeStampFrom):
        global stub
        events = []
        try:
            arg = GRPCProto_pb2.ArgEvents(assetId=assetId,
                                          timeStampFrom=timeStampFrom)
            readdata = stub.GetEvents(arg)
            for item in readdata.enentsVal:
                events.append({'TimeStamp': item.timeStamp, 'Msg': item.msg,
                               'Type': item.type, 'Cat': item.cat, 'Status': item.status,
                               'Additional': item.additional, 'EventId': item.eventId,
                               'Info': item.info, 'Trends': item.trends, 'User': item.user,
                               'Comments': item.comments, 'History': item.history})
            return events
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def GetUnAckEvents(self,assetId,timeStampFrom):
        global stub
        events = []
        try:
            arg = GRPCProto_pb2.ArgEvents(assetId=assetId,
                                          timeStampFrom=timeStampFrom)
            readdata = stub.GetUnAckEvents(arg)
            for item in readdata.enentsVal:

                events.append({'TimeStamp': item.timeStamp, 'Msg': item.msg,
                               'Type': item.type, 'Cat': item.cat, 'Status': item.status,
                               'Additional': item.additional,'EventId':item.eventId,
                               'Info':item.info,'Trends': item.trends,'User':item.user,
                               'Comments':item.comments,'History': item.history})
            return events
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def AckEvent(assetId,event):
        global stub
        try:
            #event['Trends'] = ET.tostring(event['Trends'])
            #event['History'] = ET.tostring(event['History'])
            event = GRPCProto_pb2.EventVal(timeStamp=event['TimeStamp'],type=event['Type'],
                                           cat=event['Cat'],status=event['Status'],msg=event['Msg'],
                                           additional=event['Additional'],eventId=event['EventId'],
                                           info=event['Info'],trends=event['Trends'],user=event['User'],
                                           comments=event['Comments'],history=event['History'])
            arg = GRPCProto_pb2.ArgAckEvent(assetId=assetId,
                                            event=event)
            ret = stub.AckEvent(arg)
            return ret

        except Exception as e:
            print(e)
        return False

    @staticmethod
    def VerifyUserCredentials(login,password,isAnonymousUser):
        global stub
        userParams = {'verifyRezult': False, 'login': '',
                      'password': '', 'name': '',
                      'post': '', 'role': ''}
        try:
            arg = GRPCProto_pb2.ArgUserCredentials(login=login,
                                                   password=password,
                                                   isAnonymousUser=isAnonymousUser)
            ret = stub.VerifyUserCredentials(arg)
            userParams = {'verifyRezult': ret.verifyRezult,'login': ret.login,
                          'password': ret.password,'name': ret.name,
                          'post': ret.post,'role': ret.role}
            return userParams
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def GetSourceHistDataFromServer(assetId,dateTimeFrom,dateTimeTo,idTags):
        global stub
        try:
            arg = GRPCProto_pb2.ArgDataHist(assetId=assetId,
                                            timeStampFrom = dateTimeFrom,
                                            timeStampTo = dateTimeTo,
                                            tagsId = idTags)
            data = stub.GetSourceDataHistStream(arg)
            res = []
            for response in data:
                for item in response.tagsVal:
                    res.append({'value':item.value,'tagId':item.tagId,
                            'timeStamp':item.timeStamp,'isGood':item.isGood})
            return res
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def GetSourceSliceHistDataFromServer(assetId,dateTimeFrom,dateTimeTo,idTags,countRange):
        global stub
        try:
            arg = GRPCProto_pb2.ArgSliceDataHist(assetId=assetId,
                                            timeStampFrom = dateTimeFrom,
                                            timeStampTo = dateTimeTo,
                                            tagsId = idTags,
                                            slicesCount = countRange)
            data = stub.GetSourceSliceDataHistStream(arg)
            res = []
            for response in data:
                for item in response.tagsVal:
                    res.append({'value': item.value, 'tagId': item.tagId,
                                'timeStamp': item.timeStamp, 'isGood': item.isGood})
            return res
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def GetDataStream(self,assetId,tagsId,timeStampFrom):
            global stub
        #try:
            async with grpc.aio.insecure_channel("localhost:6062") as channel:
                stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)
                arg = GRPCProto_pb2.ArgData(assetId=assetId,
                                            tagsId=tagsId[:],
                                            timeStampFrom=timeStampFrom)
                # Read from an async generator
                data = []
                async for response in stub.GetDataStream(arg):
                    print(response.tagsVal)
                    data.append(response.tagsVal)


            #channel = grpc.insecure_channel('localhost:6062')
            #stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)
            #arg = GRPCProto_pb2.ArgData(assetId=assetId,
            #                            tagsId=tagsId[:],
            #                            timeStampFrom=timeStampFrom)
            #responses = self.stub.GetDataStream(arg)

            #responses = stub.GetDataStream(arg)
            #data = []
            #for response in responses:
            #    data.append(response.tagsVal)
            #print(data)
            #return data
            #return responses
        #except Exception as e:
        #    print(e)
        #    return False


    def GetDataFromCache(self,assetId,tagId):
        return self.DataCache['asset'+str(assetId)+'tag'+str(tagId)]

    @staticmethod
    def GetDashboards(projectInfo,assetId):
        try:
            conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                    password=projectInfo['password'], host=projectInfo['host'],
                                    port=projectInfo['port'])
            cursor = conn.cursor()
            sqll = """ 
                        CREATE TABLE IF NOT EXISTS {}.Dashboards (
                            "ID"        SERIAL PRIMARY KEY,
                            "user"      INT,
                            "type"      VARCHAR ( 255 ),
                            "name"      VARCHAR ( 255 ),
                            "desc"      VARCHAR ( 255 ),
                            "config"    bytea
                        );
                   """
            cursor.execute(
                sql.SQL(sqll).format(sql.Identifier(str('Asset_'+str(assetId)))))
            #result.extend(res)
            cursor.close()
            conn.commit()

            cursor = conn.cursor()
            sqll = """ 
                SELECT "ID","user","type","name","desc","config"
                FROM {}."dashboards"
                                   """
            cursor.execute(
                sql.SQL(sqll).format(sql.Identifier(str('Asset_' + str(assetId)))))
            res = cursor.fetchall()
            # result.extend(res)
            cursor.close()
            conn.commit()
            return res
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def AddDashboard(projectInfo,assetId,dashboardInfo):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                    INSERT INTO {}.Dashboards ("user","type","name","desc","config")
                    VALUES(%s,%s,%s,%s,%s)
                    RETURNING "ID"
               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Asset_' + str(assetId)))),
            [dashboardInfo['User'],
             dashboardInfo['Type'],
             dashboardInfo['Name'],
             dashboardInfo['Desc'],
             dashboardInfo['Config']])
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def GetDashboard(projectInfo,assetId,dashboardId):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                        SELECT "ID","user","type","name","desc","config"
                        FROM {}."dashboards"
                        WHERE "ID" = %s
               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Asset_' + str(assetId)))),
            [dashboardId])
        result = cursor.fetchall()[0]
        cursor.close()
        conn.commit()
        return result
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def DeleteDashboard(projectInfo,assetId,dashboardId):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                                DELETE
                                FROM {}."dashboards"
                                WHERE "ID" = %s
                       """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Asset_' + str(assetId)))),
            [dashboardId])
        cursor.close()
        conn.commit()
        return True
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def GetGroupsDashboards(projectInfo,GroupId):
        #try:
            conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                    password=projectInfo['password'], host=projectInfo['host'],
                                    port=projectInfo['port'])
            cursor = conn.cursor()
            sqll = """ 
                        CREATE TABLE IF NOT EXISTS {}."AssetGroupsDashboards" (
                            "ID"        SERIAL PRIMARY KEY,
                            "IDAssetGroup" INT,
                            "user"      INT,
                            "type"      VARCHAR ( 255 ),
                            "name"      VARCHAR ( 255 ),
                            "desc"      VARCHAR ( 255 ),
                            "config"    bytea
                        );
                   """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets'),sql.Identifier('Assets')))
            #result.extend(res)
            cursor.close()
            conn.commit()

            cursor = conn.cursor()
            sqll = """ 
                SELECT "ID","IDAssetGroup","user","type","name","desc","config"
                FROM {}."AssetGroupsDashboards"
                WHERE "IDAssetGroup" = %s
                   """
            cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets')),[GroupId])
            res = cursor.fetchall()
            # result.extend(res)
            cursor.close()
            conn.commit()
            return res
        #except Exception as e:
         #   print(e)
         #   return False

    @staticmethod
    def AddGroupDashboard(projectInfo,GroupId,dashboardInfo):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                    INSERT INTO {}."AssetGroupsDashboards" ("IDAssetGroup","user","type","name","desc","config")
                    VALUES(%s,%s,%s,%s,%s,%s)
                    RETURNING "ID"
               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Assets'))),
            [GroupId,
             dashboardInfo['User'],
             dashboardInfo['Type'],
             dashboardInfo['Name'],
             dashboardInfo['Desc'],
             dashboardInfo['Config']])
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def GetGroupDashboard(projectInfo,dashboardId):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                        SELECT "ID","user","type","name","desc","config"
                        FROM {}."AssetGroupsDashboards"
                        WHERE "ID" = %s
               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier('Assets')),
            [dashboardId])
        result = cursor.fetchall()[0]
        cursor.close()
        conn.commit()
        return result
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def DeleteGroupDashboard(projectInfo,dashboardId):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                                DELETE
                                FROM {}."AssetGroupsDashboards"
                                WHERE "ID" = %s
                       """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Assets'))),
            [dashboardId])
        cursor.close()
        conn.commit()
        return True
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def SaveAssetDashboard(projectInfo,assetId,dashboardId,dashboardConfig):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                                        UPDATE {}."dashboards"
                                        SET "config" = %s
                                        WHERE "ID" = %s
                               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Asset_' + str(assetId)))),
            [dashboardConfig,
             dashboardId])
        cursor.close()
        conn.commit()
        return True
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def SaveGroupDashboard(projectInfo,dashboardId,dashboardConfig):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                                UPDATE {}."AssetGroupsDashboards"
                                SET "config" = %s
                                WHERE "ID" = %s
                       """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Assets'))),
            [dashboardConfig,
             dashboardId])
        cursor.close()
        conn.commit()
        return True
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def GetAssetsViewConfig(projectInfo,AssetViewId):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                                CREATE TABLE IF NOT EXISTS {}."AssetsViewConfig" (
                                    "ID"         SERIAL PRIMARY KEY,
                                    "ConfigName" VARCHAR ( 255 ),
                                    "user"      INT,
                                    "config"    bytea
                                );
                           """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets'), sql.Identifier('Assets')))
        # result.extend(res)
        cursor.close()
        conn.commit()

        cursor = conn.cursor()
        sqll = """ 
                        SELECT "ID","ConfigName","user","config"
                        FROM {}."AssetsViewConfig"
                        WHERE "ID" = %s
                           """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier('Assets')), [AssetViewId])
        res = cursor.fetchall()
        # result.extend(res)
        cursor.close()
        conn.commit()
        return res
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def SaveAssetsViewConfig(projectInfo,AssetViewId,AssetViewConfig):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                                UPDATE {}."AssetsViewConfig"
                                SET "config" = %s
                                WHERE "ID" = %s
                       """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Assets'))),
            [AssetViewConfig,
             AssetViewId])
        cursor.close()
        conn.commit()
        return True
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def AddAssetsViewConfig(projectInfo,AssetViewConfig,user):
        # try:
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sqll = """ 
                    INSERT INTO {}."AssetsViewConfig" ("ConfigName","user","config")
                    VALUES(%s,%s,%s)
                    RETURNING "ID"
               """

        cursor.execute(
            sql.SQL(sqll).format(sql.Identifier(str('Assets'))),
            ['PublicAssetView',
             0,
             AssetViewConfig])
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result
    # except Exception as e:
    #   print(e)
    #   return False

    @staticmethod
    def InitialCollection(projectInfo):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()

        sql = """ 
                                    CREATE SCHEMA IF NOT EXISTS "Collections"
                               """

        cursor.execute(sql)
        sql = """ 
                                    CREATE TABLE IF NOT EXISTS "Collections"."Templates" (
                                    "ID"                 SERIAL PRIMARY KEY,
                                    "TemplateName"       VARCHAR ( 255 ),
                                    "DisplayName"        VARCHAR ( 255 ),
                                    "IsSysTemplate"      BOOLEAN,
                                    "ParentTemplateId"   INT DEFAULT NULL,
                                    FOREIGN KEY ("ParentTemplateId")
                                    REFERENCES "Collections"."Templates"("ID")
                                    );
                               """

        cursor.execute(sql)
        sql = """ 
                                    CREATE TABLE IF NOT EXISTS "Collections"."Collections" (
                                    "ID"         SERIAL PRIMARY KEY,
                                    "Name" VARCHAR ( 255 ),
                                    "TemplateId"      INT,
                                    FOREIGN KEY ("TemplateId")
                                    REFERENCES "Collections"."Templates"("ID")
                                    ON DELETE CASCADE
                                );
                               """

        cursor.execute(sql)

        sql = """ 
                                    CREATE TABLE IF NOT EXISTS "Collections"."TemplateAttributes" (
                                    "ID"         SERIAL PRIMARY KEY,
                                    "TemplateId" INT,
                                    "AttributeName" VARCHAR ( 255 ),
                                    "DisplayName" VARCHAR ( 255 ),
                                    "AttributeType" VARCHAR ( 255 ),
                                    "DisplayType" VARCHAR ( 255 ),
                                    "IsSecondary" BOOLEAN,
                                    "IsNotNull" BOOLEAN,
                                    FOREIGN KEY ("TemplateId")
                                    REFERENCES "Collections"."Templates"("ID")
                                    ON DELETE CASCADE
                                    );
                               """
        cursor.execute(sql)
        sql = """ 
                                    INSERT INTO "Collections"."Templates" ("TemplateName","DisplayName","IsSysTemplate")
                                    SELECT %s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "TemplateName" FROM "Collections"."Templates" WHERE "TemplateName" = %s
                                    ) LIMIT 1;
                               """
        cursor.execute(sql,["Employees","Сотрудники","True","Employees"])
        cursor.close()
        conn.commit()
        cursor = conn.cursor()
        sql = """ 
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                                    INSERT INTO "Collections"."TemplateAttributes" (
                                    "TemplateId","AttributeName","DisplayName","AttributeType","DisplayType","IsSecondary","IsNotNull")
                                    SELECT %s,%s,%s,%s,%s,%s,%s
                                    WHERE NOT EXISTS (
                                    SELECT "AttributeName" FROM "Collections"."TemplateAttributes" WHERE "AttributeName" = %s
                                    ) LIMIT 1;
                               """
        cursor.execute(sql,["1","Number","Табельный номер","VARCHAR","NULL","FALSE","TRUE","Number",
                       "1","Surname","Фамилия","VARCHAR","NULL","FALSE","TRUE","Surname",
                       "1","Name","Имя","VARCHAR","NULL","FALSE","TRUE","Name",
                       "1","Patronymic","Отчество","VARCHAR","NULL","FALSE","FALSE","Patronymic",
                       "1","Position","Должность","VARCHAR","NULL","FALSE","FALSE","Position",
                       "1","Department","Подразделение","VARCHAR","NULL","TRUE","FALSE","Department"])

        sql = """   CREATE TABLE IF NOT EXISTS "Collections"."Employees" (
                    "ID"         SERIAL PRIMARY KEY,
                    "CollectionId" INT DEFAULT NULL,
                    "AssetId" INT DEFAULT NULL,
                    "AssetGroup" INT  DEFAULT NULL,
                    "Number" VARCHAR ( 255 ),
                    "Surname" VARCHAR ( 255 ),
                    "Name" VARCHAR ( 255 ),
                    "Patronymic" VARCHAR ( 255 ),
                    "Position" VARCHAR ( 255 ),
                    "Department" VARCHAR ( 255 ),
                    FOREIGN KEY ("CollectionId")
                    REFERENCES "Collections"."Collections"("ID")
                    ON DELETE CASCADE,
                    FOREIGN KEY ("AssetId")
                    REFERENCES "Assets"."Assets"("ID"),
                    FOREIGN KEY ("AssetGroup")
                    REFERENCES "Assets"."AssetGroups"("ID")
                    );
        """
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        return True

    @staticmethod
    def AddCollection(projectInfo,CollName,TemplateId):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll ="""
                            INSERT INTO "Collections"."Collections" ("Name","TemplateId")
                            VALUES(%s,%s)
                            RETURNING "ID"
                        """
        cursor.execute(sqll, [CollName,TemplateId])

        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result

    @staticmethod
    def DeleteCollection(projectInfo,CollectionId):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                                        DELETE
                                        FROM "Collections"."Collections"
                                        WHERE "ID" = %s
                               """

        cursor.execute(sqll,[CollectionId])
        cursor.close()
        conn.commit()
        return True

    @staticmethod
    def GetCollections(projectInfo):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                                SELECT "ID","Name","TemplateId"
                                FROM "Collections"."Collections"
                       """

        cursor.execute(sqll)
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        collections = []
        for coll in result:
            collections.append({'Id':coll[0],'Name':coll[1],'TemplateId':coll[2]})
        return collections

    @staticmethod
    def GetTemplates(projectInfo):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                                        SELECT "ID","TemplateName","DisplayName","IsSysTemplate","ParentTemplateId"
                                        FROM "Collections"."Templates"
                               """

        cursor.execute(sqll)
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        templates = []
        for item in result:
            templates.append({'Id':item[0],'TemplateName':item[1],'DisplayName':item[2],
                              'IsSysTemplate':item[3],'ParentTemplateId':item[4]})
        return templates

    @staticmethod
    def GetTemplateAttributes(projectInfo,TemplateId):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                            SELECT *
                            FROM "Collections"."TemplateAttributes"
                            WHERE "TemplateId" = %s
                   """
        cursor.execute(sqll, [TemplateId])
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        templateAttributes = []
        for item in result:
            templateAttributes.append({'Id':item[0],'TemplateId':item[1],'AttributeName':item[2],
                                       'DisplayName':item[3],'AttributeType':item[4],
                                       'DisplayType':item[5],'IsSecondary':item[6],
                                       'IsNotNull':item[7]})
        return templateAttributes

    @staticmethod
    def GetCollectionElements(projectInfo,CollId,TemplateName):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        sqll = """ 
                    SELECT *
                    FROM "Collections".{}
                    WHERE "CollectionId" = %s
           """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(str(TemplateName))),[CollId])
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result

    @staticmethod
    def AddCollectionElement(projectInfo,CollId, TemplateName, AssetId, GroupId,ElementAttributes):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        insertString = '%s,'
        if AssetId != None:
            insertString += '%s,'
        else:
            insertString += 'default,'
        if GroupId != None:
            insertString += '%s,'
        else:
            insertString += 'default,'
        for elem in ElementAttributes:
                insertString += '%s,'
        insertString = insertString[0:-1]
        if GroupId != None:
            ElementAttributes.insert(0,str(GroupId))
        if AssetId != None:
            ElementAttributes.insert(0,str(AssetId))
        ElementAttributes.insert(0,str(CollId))
        sqll ="""
                            INSERT INTO "Collections".{}
                            VALUES(default,""" + insertString + """)
                            RETURNING "ID"
                        """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(str(TemplateName))),ElementAttributes)
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return result

    @staticmethod
    def DelCollectionElement(projectInfo,TemplateName,ElemId):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        print(TemplateName,'\n',type(TemplateName))
        print(ElemId,'\n',type(ElemId))
        sqll = """ 
                    DELETE
                    FROM "Collections".{}
                    WHERE "ID" = %s
           """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(str(TemplateName))), [str(ElemId)])
        cursor.close()
        conn.commit()
        return True

    @staticmethod
    def EditCollectionElement(projectInfo, AttributesKeys, TemplateName, ElementAttributes, ElemId):
        conn = psycopg2.connect(database=projectInfo['database'], user=projectInfo['user'],
                                password=projectInfo['password'], host=projectInfo['host'],
                                port=projectInfo['port'])
        cursor = conn.cursor()
        insertString = ''
        for i in range(0, len(AttributesKeys)):
            if ElementAttributes[i] != '':
                insertString += '"' + AttributesKeys[i] + '" = ' + ElementAttributes[i] + ','
            else:
                insertString += '"' + AttributesKeys[i] + '" = default,'
        insertString = insertString[:-1]
        sqll ="""
                            UPDATE "Collections".{}
                            SET """ + insertString + """
                            WHERE "ID" = %s
                        """
        cursor.execute(sql.SQL(sqll).format(sql.Identifier(str(TemplateName))), [str(ElemId)])
        cursor.close()
        conn.commit()
        return True


def on_connectivity_change(value):
    state = str(value)
    print("connection changed: " + state)
    return

def AppendGroups(group,AssetGroups):
    if group[0].get('ParentId') != None:
        for group1 in AssetGroups:
            if group1['ParentId'] == group[0]['Id'] and group1 not in group[1]:
                group[1].append([group1, []])
    return group


def AppendAssets(group,Assets):
    for asset in Assets:
        if asset['GroupId'] == group[0]['Id'] and asset not in group[1]:
            group[1].append([asset])
    return group



# ОСНОВНАЯ ФУНКЦИЯ
def run():


    client = ClientGrpc
    print('connect: '+ str(client.Connect(client,'localhost','6062','str')))

    #client.Disconnect(client,'str')

    #type(client.StateConnect(client))

    #print('disconnect:' + str(client.Disconnect(client, 'str')))
    projectinfo = client.GetProjectInfo(client)

    #print('PROJECTINFO: '+str(projectinfo))
    #print('GetAssets: '+str(client.GetAssets(client)))
    #print('GetAssetGroups: '+str(client.GetAssetGroups(client,1)))
    #asset1 = client.GetAssetHistInfo(client,1)
    #print(client.InitialCollection(client,projectinfo))
    #print(client.AddCollection(client, projectinfo, 'CollName', 'Employees'))
    #print(client.DeleteCollection(client,projectinfo,1))
    print(client.GetCollections(client,projectinfo))
    #print(client.GetAssetGroupsFromPostgreSQL(client, projectinfo))
    #project = client.GetProjectInfo(client)
    #assets = client.GetAssetsFromPostgreSQL(client, project)
    #print(projectinfo)
    #print(client.GetDasboards(client,projectinfo,1))
    #print(client.AddGroupDashboard(client,projectinfo,1,{'Name':'name','Desc':'desc','Config':bytes(1),'User':1,'Type':'hist'}))
    #assetGroups = client.GetAssetGroupsFromPostgreSQL(client, project)
    #assetList = []


    #print(client.GetGroupsDashboards(client,project,1))
    #print(client.DeleteGroupDashboard(client,project,1))
    #print(asset1)
    #t2 = client.GetAssetHistLastDateTime(client,asset1)
    #print(t2,'\n',type(t2))
    #t1 = client.GetAssetHistFirstDateTime(client, asset1)
    #print(t1, '\n', type(t1))
    #t1 = datetime(1970,1,1)
    #t2 = datetime.now()
    #print(client.GetSourceHistDataFromServer(client,1,t1,t2,[1]))
    #print(client.GetHistEvents(client,asset1,t1,t2))
    #print(hist)
    #print(client.GetHistData(client,21,asset1,t1,t2,[1]))
   # print(client.GetSliceHistData(client,1,asset1,t1,t2,[1,2],10,10))
   # print(client.GetTagGroups(client,1))
    #wrap = client.GetDataStream(client,10,[1,4,5,10],1000)
    #arg = GRPCProto_pb2.ArgData(assetId=10,
    #                            tagsId=[1],
    #                            timeStampFrom=10000)
    #print(client.GetTags(client,1))
    #async with aio.insecure_channel('localhost:6061') as channel:

        #stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)
        #stream = stub.GetDataStream(arg)
        #print(stream)
        #task = asyncio.create_task(stream.read())
        #await client
        #    read = stream.ResponseStream.Current
        #print(read.next())
        #await client.GetDataStream(client,10,[1],1000,stub)

        #await client.GetDataSnapShot(client, 10, [1,4],stub)
      #  await asyncio.gather(
      #      client.GetDataStream(client, 10, [1], 1000, stub),
      #      client.GetDataSnapShot(client, 10, [1],stub)
      #  )
    #print(client.GetDataStream(client,5,[1],100))
    #print(client.GetData(client,10,[1],1630524037))
    #print(client.GetEvents(client,1,10000))
    #print(client.GetUnAckEvents(client,1,10000))
    #event = client.GetUnAckEvents(client,1,10000)
    #print(client.AckEvent(client,1,event))
    #print(client.GetEvents(client, 1, 1))
    #print(client.VerifyUserCredentials(client,'','',True))


if __name__ == '__main__':
    logging.basicConfig()
    #asyncio.get_event_loop().run_until_complete(run())
    run()
