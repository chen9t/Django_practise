# -*- coding: utf-8 -*-
import copy

import requests
from requests.exceptions import Timeout
from lxml import etree

from vehicle_violation_query.models import CarInfo
from insurance_query.models import InsuranceInfo

from insurance_query.query_settings import SERVICE_URL
from insurance_query.query_settings import TIME_OUT
from insurance_query.query_settings import QUERY_TYPE


class GetXMLResponse(object):

    def __init__(self, query_type, **kwargs):

        self.query_type = query_type
        self.query_fileds = kwargs

    def get_xml_stream(self):
        request_string = self.form_request_content()
        xml_stream = self.send_requests(request_string)

        return xml_stream

    def form_request_content(self):
        """ 请求的xml内容 """
    
        doc = etree.fromstring('<?xml version="1.0" encoding="GBK"?><Packet>'\
                            '<Head><RequestType>V002</RequestType><User>youke'\
                            '</User><Password>000000</Password></Head>'\
                            '<Body><BasePart></BasePart></Body></Packet>')
                           
        param_elem = doc.xpath('//BasePart')[0]
        qt_elem = doc.makeelement('QueryType')
        qt_elem.text = '0' + QUERY_TYPE[self.query_type]
        param_elem.append(qt_elem)

        if self.query_type=='by_policeno':
            subelem = doc.makeelement('PolicyNo')
            subelem.text = self.query_fileds['policy_no']
            param_elem.append(subelem)

        elif self.query_type=='by_licenseno_VIN':
            subelem = doc.makeelement('LicenseNo')
            subelem.text = self.query_fileds['license_no']
            param_elem.append(subelem)
            subelem = doc.makeelement('FrameLastSixNo')
            subelem.text = self.query_fileds['VIN_last_six']
            param_elem.append(subelem)

        elif self.query_type=='by_VIN_engineno':
            subelem = doc.makeelement('FrameLastSixNo')
            subelem.text = self.query_fileds['VIN_last_six']
            param_elem.append(subelem)
            subelem = doc.makeelement('EngineLastSixNo')
            subelem.text = self.query_fileds['engine_last_six_no']
            param_elem.append(subelem)
        
        else:
            subelem = doc.makeelement('FrameNo')
            subelem.text = self.query_fileds['VIN']
            param_elem.append(subelem)
        
        subelem = doc.makeelement('PageNo')
        subelem.text = self.query_fileds.get('pageno', '1')
        param_elem.append(subelem)
        
        return etree.tostring(doc, encoding='GBK', xml_declaration=True,)

    def send_requests(self, request_string):
        '''发送请求,并获得数据'''

        headers = {
            'content-Type': 'appliation/xml;charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'
        }

        try:
            r = requests.post(SERVICE_URL, data=request_string, headers=headers,timeout=TIME_OUT)
        except Timeout:
            raise Timeout

        if r.status_code == 200:
            return r.content
        else:
            r.raise_for_status()


class ParseXML(object):

    def __init__(self, xml_stream):
        self._doctree = etree.fromstring(xml_stream)

    @property  
    def error(self):
        """ 
        判断请求内容是否有误
        
        @return: 错误：{错误码:错误消息}；成功:None
        """
        
        if not int(self._doctree.xpath('//ResponseCode')[0].text):
            errmsg = self._doctree.xpath('//ErrorMessage')[0].text
            return errmsg,
        else:
            return None
        
    @property      
    def totalpage(self):
        """ 总的页数 """
        return int(self._doctree.xpath('//TotalPage')[0].text)
    
    @property  
    def pageno(self):
        """ 当前文档的页数号 """
        return int(self._doctree.xpath('//PageNo')[0].text)
    
    @property  
    def totalelems(self):
        """ 当前文档的总保险单号数目 """
        return int(self._doctree.xpath('//TotalCount')[0].text)
    
    @property
    def elems(self):
        """ 得到当前文档包含的保险单号元素
        
        每个元素的内容列表包括：
        PolicyNo[M]         保单号
        OperateDate[M]      签单时间
        StartDate[M]        起保时间
        EndDate[M]          终保时间
        LicenseNo[M]        车牌号
        CompanyCode[M]      承保公司
        RiskType[M]         险种类型
        
        ClaimStatus[O]      案件状态
        ClaimQueryNo[O]     理赔编码
        EstimateLoss[O]     赔款金额
        SumPaid[O]          总付款
        DamageDate[O]       出险时间
        ReportDate[O]       报案时间
        ClaimDate[O]        立案时间
        EndcaseDate[O]      结案时间
        DriverName[O]       损害赔偿责任
        """
        res = []
        for elem in self._doctree.xpath('//ClaimData'):
            elem_dic = {}
            for chelem in elem:
                elem_dic[chelem.tag] = chelem.text
            res.append(elem_dic)
        return res


class StoreInfo(object):

    def __init__(self, query_type, **kwargs):

        self.query_type = query_type
        self.query_fileds = kwargs

    def store_car_info1(self):

        license_no = self.query_fileds['license_no']
        VIN_last_six = self.query_fileds['VIN_last_six']

        car_info, created = CarInfo.objects.get_or_create(license_plate_num=license_no,
            defaults={'VIN_last_six': VIN_last_six})

        if not created:
            if not car_info.VIN_last_six:
                car_info.VIN_last_six = VIN_last_six
                car_info.save()

        return (car_info, created)

    def store_car_info2(self):

        VIN = self.query_fileds['VIN']
        car_info, created = CarInfo.objects.get_or_create(VIN=VIN)

        return (car_info, created)

    def store_insurance_info(self, car_info, car_not_exists, record_list):

        candidate_list = copy.deepcopy(record_list)
        need_to_insert = []
        claim_query_no_list = []
        policy_no_list = []
        insert_list = []

        if car_not_exists: # New car, insert all
            need_to_insert = candidate_list
        else: # Old cars, check if there are records
            old_record_list = InsuranceInfo.objects.filter(LicenseNo=car_info)

            if old_record_list.exists(): # Old record exists

                for old_record in old_record_list: # Get the old records
                    claim_query_no_list.append(old_record.ClaimQueryNo)
                    policy_no_list.append(old_record.PolicyNo)

                for record in candidate_list:
                    claim_query_no = record.get('ClaimQueryNo', '')
                    if claim_query_no: # Valid record
                        if claim_query_no not in claim_query_no_list: # New record
                            need_to_insert.append(record)
                        else: # Record already exists
                            o_record = InsuranceInfo.objects.get(ClaimQueryNo=claim_query_no)

                            if o_record.ClaimStatus != record['ClaimStatus']:
                                # Update record when status changes.
                                o_record.ClaimStatus = record.get('ClaimStatus', '')
                                o_record.PolicyNo = record.get('PolicyNo', '')
                                o_record.OperateDate = record.get('OperateDate', '')
                                o_record.StartDate = record.get('StartDate', '')
                                o_record.EndDate = record.get('EndDate', '')
                                o_record.CompanyCode = record.get('CompanyCode', '')
                                o_record.DamageDate = record.get('DamageDate', '')
                                o_record.ReportDate = record.get('ReportDate', '')
                                o_record.EstimateLoss = record.get('EstimateLoss', '')
                                o_record.ClaimDate = record.get('ClaimDate', '')
                                o_record.EndcaseDate = record.get('EndcaseDate', '')
                                o_record.RiskType = record.get('RiskType', '')
                                o_record.DriverName = record.get('DriverName', '')
                                o_record.SumPaid = record.get('SumPaid')
                                o_record.IndemnityDuty = record.get('IndemnityDuty', '')

                                o_record.save()

            else: # No old records, insert all
                need_to_insert = candidate_list

        if need_to_insert:
            for new_record in need_to_insert:
                if new_record.get('ClaimQueryNo', ''):
                    new_record.update(LicenseNo=car_info)
                    insurance_info = InsuranceInfo(**new_record)
                    insert_list.append(insurance_info)

            InsuranceInfo.objects.bulk_create(insert_list)
