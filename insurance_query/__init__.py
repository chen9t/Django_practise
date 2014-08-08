# -*- coding: utf-8 -*-
import requests
from requests.exceptions import Timeout
from lxml import etree

from insurance_query.models import CarInfo
from insurance_query.models import InsuranceInfo


SERVICE_URL = 'http://106.37.176.173:9080/phoneserver/phserver'
TIME_OUT = 10


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
        assert(int(self.query_type) in range(1, 5))
    
        doc = etree.fromstring('<?xml version="1.0" encoding="GBK"?><Packet>'\
                            '<Head><RequestType>V002</RequestType><User>youke'\
                            '</User><Password>000000</Password></Head>'\
                            '<Body><BasePart></BasePart></Body></Packet>')
                           
        param_elem = doc.xpath('//BasePart')[0]
        qt_elem = doc.makeelement('QueryType')
        qt_elem.text = '0'+self.query_type
        param_elem.append(qt_elem)
    
        if self.query_type=='1':
            subelem = doc.makeelement('PolicyNo')
            subelem.text = self.query_fileds['policy_no']
            param_elem.append(subelem)
        
        elif self.query_type=='2':
            subelem = doc.makeelement('LicenseNo')
            subelem.text = self.query_fileds['license_no']
            param_elem.append(subelem)
            subelem = doc.makeelement('FrameLastSixNo')
            subelem.text = self.query_fileds['frame_last_six_no']
            param_elem.append(subelem)
        
        elif self.query_type=='3':
            subelem = doc.makeelement('FrameLastSixNo')
            subelem.text = self.query_fileds['frame_last_six_no']
            param_elem.append(subelem)
            subelem = doc.makeelement('EngineLastSixNo')
            subelem.text = self.query_fileds['engine_last_six_no']
            param_elem.append(subelem)
        
        else:
            subelem = doc.makeelement('FrameNo')
            subelem.text = self.query_fileds['frame_no']
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

    def store_car_info(self):

        license_no = self.query_fileds['license_no']
        frame_last_six_no = self.query_fileds['frame_last_six_no']

        car_info, created = CarInfo.objects.get_or_create(license_no=license_no,
            defaults={'frame_last_six_no': frame_last_six_no})

        return (car_info.license_no, created)

    def store_insurance_info(self, license_no, car_not_exists, record_list):

        need_to_insert = []
        claim_query_no_list = []

        if car_not_exists: # New car, insert all
            need_to_insert = record_list
        else: # Check if there are records
            old_record_list = InsuranceInfo.objects.filter(car_info=license_no)

        if old_record_list.exists(): # Old record exists

            for old_record in old_record_list: # Get the old records
                claim_query_no_list.append(old_record.claim_query_no)

            for record in record_list:
                claim_query_no = record.get('claim_query_no', '')
                if claim_query_no: # Valid record
                    if claim_query_no not in claim_query_no_list: # New record
                        need_to_insert.append(record)
                    else: # Record already exists
                        o_record = InsuranceInfo.objects.get(claim_query_no=claim_query_no)
                        if o_record.claim_status != record['claim_status']:
                            o_record.update(
                                claim_status=record.get('claim_status', ''),
                                estimate_loss=record.get('estimate_loss', ''),
                                claim_date=record.get('claim_date', ''),
                                end_case_date=record.get('end_case_date', ''),
                                dirver_name=record.get('dirver_name', ''),
                                sum_paid=record.get('sum_paid'),
                                indemnity_duty=record.get('indemnity_duty', ''))
        else: # No old records, insert all
            need_to_insert = record_list


        # need_to_insert = []
        # finsihed_records = []
        # claim_query_no_list = []
        # insert_list = []

        # for record in record_list:
        #     claim_status = record_list.get('claim_status', '')
        #     if claim_status == u'已结案':
        #         finsihed_records.append(record)

        # if finsihed_records:
        #     if car_not_exists:
        #         need_to_insert = finsihed_records
        #     else:
        #         old_record_list = InsuranceInfo.objects.filter(car_info=license_no)
        #         for old_record in old_record_list:
        #             claim_query_no_list.append(old_record.claim_query_no)
        #         for finished_record in finsihed_records:
        #             if finished_record.claim_query_no not in claim_query_no_list:
        #                 need_to_insert.append(finished_record)

        if need_to_insert:
            for new_record in need_to_insert:
                insurance_info = InsuranceInfo(**new_record)
                insert_list.append(insurance_info)

        InsuranceInfo.objects.bulk_create(insert_list)

if __name__ == '__main__':
    res = GetXMLResponse('2', licenseno=u'苏A7ZA68', framelastsix='242191')
    xml_stream = res.get_xml_stream()
    print xml_stream
