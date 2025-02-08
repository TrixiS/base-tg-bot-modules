class BotChat(Model):
    id = fields.BigIntField(
        pk=True, unique=True, generated=False
    )  # telegram chat id signed
    title = fields.TextField()
    username = fields.TextField(null=True)
    type = fields.TextField()
