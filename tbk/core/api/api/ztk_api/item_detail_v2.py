from typing import Optional, List

from asgiref.sync import sync_to_async
from django.http import HttpRequest
from pydantic import Field
from qiyu_api.ztk_api import ItemDetailV2Args, ItemDetailV2Model

from core.logger import get_logger
from core.resp.base import ApiResp, ResponseModel
from core.shared import AppErrno
from core.vendor.ztk import get_ztk_api
from ...api.app import app
from ...api_utils import api_inner_wrapper

__all__ = ["item_detail_v2"]


class ItemV2ResponseModel(ResponseModel):
    data: Optional[List[ItemDetailV2Model]] = Field(None, title="详细数据")


@app.get(
    "/ztk/item_v2",
    tags=["折淘客"],
    summary="商品详情",
    description="获取指定商品的详情\n注意: 当前仅仅支持淘宝的商品",
)
async def item_detail_v2(request: HttpRequest, item_id: str) -> ItemV2ResponseModel:
    logger = get_logger()

    ztk = await sync_to_async(get_ztk_api)(logger)

    @api_inner_wrapper(logger)
    async def inner():
        args = ItemDetailV2Args(tao_id=item_id)
        j = await ztk.item_detail_v2(args)
        if j.status == 200:
            return ApiResp.from_data(j.content)
        else:
            return ApiResp.from_errno(AppErrno.ztk_error, "请求详细数据失败")

    return await inner
