from ..middleware import admin

root_router.message.outer_middleware.register(admin.admin_middleware)
root_router.callback_query.outer_middleware.register(admin.admin_middleware)
