Get Shop Video Performance List

Returns a list of videos and associated metrics for a shop.

202605

GET

/analytics/202605/shop_videos/performance

Request Example:

curl -X GET \
 'https://open-api.tiktokglobalshop.com/analytics/202605/shop_videos/performance?sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&start_date_ge=2024-09-01&end_date_lt=2024-09-08&sort_field=gmv&currency=USD&page_token=cGFnZV9udW1iZXI9MQ==&timestamp=1623812664&app_key=38abcd&page_size=10&sort_order=DESC&account_type=ALL' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

Response Example:

{
  "code": 0,
  "data": {
    "videos": [
      {
        "id": "172xxxxxxxxxxxxx089",
        "title": "Video Title",
        "username": "Video Username",
        "creator": {
          "open_id": "uACafQAAAABmUU2qon4R0vUYvUVS3QC6CICP2m5A2-wd77j8R9G0yg",
          "user_name": "abc",
          "nick_name": "abc_bec",
          "author_type": "OFFICIAL"
        },
        "video_post_time": "2025-01-01 00:00:00",
        "duration": 34,
        "hash_tags": [
          "#racuntiktok",
          "fyp"
        ],
        "gmv": {
          "amount": "0",
          "currency": "USD"
        },
        "gpm": {
          "amount": "0",
          "currency": "USD"
        },
        "avg_customers": 0,
        "sku_orders": 0,
        "items_sold": 0,
        "views": 0,
        "click_through_rate": "0",
        "products": [
          {
            "id": "105xxxxxxxxxxxxx247",
            "name": "Product Name"
          }
        ]
      }
    ],
    "latest_available_date": "2024-09-07",
    "next_page_token": "cGFnZV9udW1iZXI9MQ==",
    "total_count": 10
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}


Error Code:

28001022: invalid request params; detail: start time or end time is invalid.
36009003: Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support.