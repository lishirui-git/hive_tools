-- 表名: rpt_nh_all_info_dsa
-- 表中文名: 信息表
SELECT
    data_date, --日期(string)
    dp,  -- 端 (string)
    user_type,  -- 用户类型 (string)
    download_type,  -- 下载类型 (string)
    download_channel,  --  二级渠道 (string)
    sub_download_channel, -- 三级渠道  (string)
    pv, -- pv (int)
    uv, -- uv (int)
    sj, -- sj (int)
    sj_uv, -- 商机uv (int)
    tel, -- 400商机 (int)
    im, -- im商机 (int)
    liuzi -- 留资商机 (int)
FROM(
select DISTINCT
new.riqi as riqi, -- 分配日期
new.time as times, -- 分配时间
from
(select
t1.riqi,
t1.time,
t3.cityid,
t1.chance_id,
t3.chance_type,
t1.agent_id,
t1.sjwh_status,
t2.CORP_NAME,
t2.MARKETING_NAME,
t2.AREA_NAME,
t2.SHOP_NAME,
t2.TEAM_NAME,
t1.qiangdantime,
t1.call_reply_time,
t1.im_reply_time
from
(SELECT
SUBSTR(ctime,1,10) as riqi,
SUBSTR(ctime,12,19) as time,
chance_id,
agent_id,
case when status=0 then '待处理'
     when status=1 then '已处理'
     when status=2 then '已回收'
     when status=3 then '不回收'
   when status=4 then '点击回拨'
   when status=5 then '加私'
   when status=6 then '标客源无效'
   else null end as sjwh_status,
ctime as qiangdantime,
case when call_reply_time='2018-01-01 00:00:00' then ''
     else call_reply_time end as call_reply_time,
case when im_reply_time='201811' then ''
     else im_reply_time end as im_reply_time
FROM ods.ods_lianjia_newhouse_service_apollo_link_business_chance_success_da
WHERE
pt= '20181120000000') t1
left join
(SELECT
uc_id,
CORP_NAME,
MARKETING_NAME,
AREA_NAME,
SHOP_NAME,
TEAM_NAME
FROM dw.dw_nh_uc_agent_info_da
WHERE
pt= '20181120000000'
and dp in ('4','5','6')) t2
on t1.agent_id=t2.uc_id
left join
(select
id,
chance_type,
SUBSTR(city_district_map,3,6) as cityid
FROM ods.ods_lianjia_newhouse_service_apollo_link_business_chance_list_da
WHERE
pt= '20181120000000') t3
on t3.id=t1.chance_id) new

left join
(select
t.chance_id,
t.agent_id,
t.uc_id,
t.customer_id,
case when t.customer_id is null then '未加私'
     when t.customer_id is not null then '已加私'
   else null end as jiasistatus,
case when status='0' then '无效'
     else '有效' end as sikebiaojishifouyouxiao
from
(select
t1.chance_id,
t1.agent_id,
t1.uc_id,
t1.ctime,
t2.customer_id,
t2.status
from
(select
a.chance_id,
a.agent_id,
b.uc_id,
a.ctime
from
(select
chance_id,
agent_id,
ctime
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_success_da
where
pt='20181120000000') a
left join
(select
id,
uc_id
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_list_da
where
pt='20181120000000') b
on a.chance_id=b.id) t1
left join
(select
agent_id,
ucid,
ctime,
customer_id,
status
FROM dw.dw_nh_customer_info_da
WHERE
pt= '20181120000000'
and if_add_customer='1') t2
on t1.agent_id=t2.agent_id
and t1.uc_id=t2.ucid
WHERE t1.ctime<=t2.ctime
) t
where
t.uc_id not in ('0')) c  -- 加私数据
on new.chance_id=c.chance_id
and new.agent_id=c.agent_id
left join
(select DISTINCT
t.chance_id,
t.agent_id,
t.uc_id,
t1.visit_id,
t1.visit_time
from
(select
a.chance_id,
a.agent_id,
b.uc_id,
a.ctime
from
(select
chance_id,
agent_id,
ctime
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_success_da
where
pt='20181120000000') a
left join
(select
id,
uc_id
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_list_da
where
pt='20181120000000') b
on a.chance_id=b.id) t
left join
(select
a.visit_agent_ucid,
b.ucid,
a.visit_id,
a.visit_time
from
(select
visit_id,
visit_time,
visit_agent_ucid,
customer_phone
from dw.dw_nh_visit_info_da
where
pt= '20181120000000'
and audit_status in ('1','2')) a
left join
(select
agent_id,
ucid,
customer_id,
customer_phone,
status
FROM dw.dw_nh_customer_info_da
WHERE
pt= '20181120000000'
and if_add_customer='1') b
on b.customer_phone=a.customer_phone) t1
on t1.visit_agent_ucid=t.agent_id
and t1.ucid=t.uc_id
WHERE t.ctime<=t1.visit_time
and t.uc_id not in ('0')) d   --带看数据
on new.chance_id=d.chance_id
and new.agent_id=d.agent_id
left join
(select DISTINCT
t.chance_id,
t.agent_id,
t.uc_id,
t1.deal_id,
t1.deal_time
from
(select
a.chance_id,
a.agent_id,
b.uc_id,
a.ctime
from
(select
chance_id,
agent_id,
ctime
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_success_da
where
pt='20181120000000') a
left join
(select
id,
uc_id
from ods.ods_lianjia_newhouse_service_apollo_link_business_chance_list_da
where
pt='20181120000000') b
on a.chance_id=b.id) t
left join
(select
a.deal_agent_ucid,
b.ucid,
a.deal_id,
a.if_deal,
a.deal_time
from
(select
deal_agent_ucid,
customer_phone,
deal_id,
if_deal,
deal_time
from dw.dw_nh_deal_info_da
WHERE
pt= '20181120000000'
and if_deal=1) a
left join
(select
agent_id,
ucid,
customer_id,
customer_phone,
status
FROM dw.dw_nh_customer_info_da
WHERE
pt= '20181120000000'
and if_add_customer='1') b
on b.customer_phone=a.customer_phone) t1
on t1.deal_agent_ucid=t.agent_id
and t1.ucid=t.uc_id
WHERE t.ctime<=t1.deal_time
and t.uc_id not in ('0')) e -- 成交数据
on new.chance_id=e.chance_id
and new.agent_id=e.agent_id