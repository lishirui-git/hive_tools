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
