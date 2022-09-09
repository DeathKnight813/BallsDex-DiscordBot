import os
import json
from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Field, Link, Model, Action
from fastapi_admin.widgets import displays, filters, inputs
from starlette.requests import Request
from ballsdex.core.models import BallInstance, User, Ball, Player, GuildConfig
from typing import List


@app.register
class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"


upload = FileUpload(uploads_dir=os.path.join(".", "static", "uploads"))
with open("ballsdex/core/admin/capacity-ref.json") as f:
    ref = json.loads(f.read())


@app.register
class AdminResource(Model):
    label = "Admin"
    model = User
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "Admins"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)


@app.register
class BallResource(Model):
    label = "Ball"
    model = Ball
    icon = "fas fa-globe"
    page_pre_title = "ball list"
    page_title = "Balls"
    filters = [
        filters.Search(
            name="country",
            label="Country",
            search_mode="contains",
            placeholder="Search for balls",
        ),
    ]
    fields = [
        "country",
        "regime",
        "economy",
        "health",
        "attack",
        "rarity",
        Field(
            name="emoji_id",
            label="Emoji ID",
        ),
        Field(
            name="wild_card",
            label="Wild card",
            display=displays.Image(width="40"),
            input_=inputs.Image(upload=upload, null=True),
        ),
        Field(
            name="collection_card",
            label="Collection card",
            display=displays.Image(width="40"),
            input_=inputs.Image(upload=upload, null=True),
        ),
        Field(
            name="credits",
            label="Image credits",
        ),
        Field(
            name="capacity_name",
            label="Capacity name",
        ),
        Field(
            name="capacity_description",
            label="Capacity description",
        ),
        # Field(
        #     name="capacity_logic",
        #     label="Capacity logic",
        #     input_=inputs.Json(
        #         null=True,
        #         options={
        #             "schema": ref,
        #             "allowSchemaSuggestions": "true",
        #             "mode": "tree",
        #             "modes": ["tree", "view", "form", "code", "text", "preview"],
        #         },
        #     ),
        # ),
    ]

    async def get_actions(self, request: Request) -> List[Action]:
        actions = await super().get_actions(request)
        actions.append(
            Action(
                icon="fas fa-upload",
                label="Generate card",
                name="generate",
                method=Method.GET,
                ajax=False,
            )
        )
        return actions


@app.register
class BallInstanceResource(Model):
    label = "Ball instance"
    model = BallInstance
    icon = "fas fa-globe"
    page_pre_title = "ball instances list"
    page_title = "Ball instances"
    filters = [
        filters.Search(
            name="ball",
            label="Ball",
            search_mode="contains",
            placeholder="Search for balls",
        ),
    ]
    fields = [
        "id",
        "ball",
        "player",
        "count",
        "catch_date",
        "special",
        "health_bonus",
        "attack_bonus",
    ]


@app.register
class PlayerResource(Model):
    label = "Player"
    model = Player
    icon = "fas fa-user"
    page_pre_title = "player list"
    page_title = "Players"
    filters = [
        filters.Search(
            name="discord_id",
            label="ID",
            search_mode="contains",
            placeholder="Filter by ID",
        ),
    ]
    fields = [
        "discord_id",
        "balls",
    ]


@app.register
class GuildConfigResource(Model):
    label = "Guild config"
    model = GuildConfig
    icon = "fas fa-cog"
    page_title = "Guild configs"
    filters = [
        filters.Search(
            name="guild_id",
            label="ID",
            search_mode="contains",
            placeholder="Filter by ID",
        ),
    ]
    fields = ["guild_id", "spawn_channel", "enabled"]
