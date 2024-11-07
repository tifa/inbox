import json
import logging

from nicegui import events, ui

from inbox.model import EmailStatus
from inbox.service.admin import (
    delete_email,
    list_domains,
    list_emails,
    upsert_email,
)
from inbox.views.notify import notify_error, notify_success

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


MASKED_PASSWORD = "*" * 10

def email():
    columns = [
        {
            "name": "username",
            "label": "Username",
            "field": "username",
            "sortable": True,
        },
        {"name": "password", "label": "Password", "field": "password"},
        {
            "name": "domain",
            "label": "Domain",
            "field": "domain",
            "sortable": True,
        },
        {
            "name": "forward_to",
            "label": "Forward to",
            "field": "forward_to",
            "sortable": True,
        },
        {
            "name": "status",
            "label": "Status",
            "field": "status",
            "sortable": True,
        },
        {"name": "description", "label": "Description", "field": "description"},
    ]

    emails = list_emails()
    domains = list_domains()

    domains_by_id = {domain.id: domain.name for domain in domains}

    rows = [
        {
            "id": email.id,
            "username": email.username,
            "password": email.password,
            "domain": {
                "label": domains_by_id.get(email.domain.id),
                "value": email.domain.id,
            },
            "forward_to": email.forward_to,
            "status": {
                "label": EmailStatus(email.status).name,
                "value": email.status,
            },
            "description": email.description,
        }
        for email in emails
    ]

    domain_options = [
        {"label": domain.name, "value": domain.id} for domain in domains
    ]
    domain_options_json = json.dumps(domain_options)

    email_status_options = [
        {"label": status.name, "value": status.value} for status in EmailStatus
    ]
    email_status_options_json = json.dumps(email_status_options)

    def add_ui_row() -> None:
        new_id = max((dx["id"] for dx in rows), default=-1) + 1
        row = {
            "id": new_id,
            "username": "",
            "password": "",
            "domain": "",
            "forward_to": "",
            "status": EmailStatus.active.name,
            "description": "",
            "is_editing": True,
            "password_visible": False,
        }
        rows.append(row)

        notify_success("Created row", str(row))
        table.update()

    def update_ui_display(e: events.GenericEventArguments) -> None:
        for row in rows:
            if row["id"] == e.args["id"]:
                row.update(e.args)
                log.debug(f"Updated UI display: {row}")
                break
        table.update()

    def delete(e: events.GenericEventArguments) -> None:
        rows[:] = [row for row in rows if row["id"] != e.args["id"]]
        try:
            delete_email(e.args["id"])
        except Exception as ex:
            notify_error("Error deleting row", str(ex))
        else:
            notify_success("Deleted row", str(e))
            table.update()

    def save(e: events.GenericEventArguments):
        try:
            for row in rows:
                if row["id"] == e.args["id"]:
                    row["is_editing"] = False
                    upsert_email(
                        id=row["id"],
                        username=row["username"],
                        password=row["password"],
                        domain_id=row["domain"]["value"],
                        forward_to=row["forward_to"],
                        status=EmailStatus(row["status"]["value"]),
                        description=row["description"],
                    )
                    break
        except Exception as e:
            row["password"] = MASKED_PASSWORD
            notify_error("Error saving row", str(e))
        else:
            notify_success("Saved row", str(row))
            table.update()

    def edit(e: events.GenericEventArguments):
        for row in rows:
            if row["id"] == e.args["id"]:
                row["is_editing"] = True
                break
        table.update()

    ui.button(
        "Add email", icon="add", color="accent", on_click=add_ui_row
    ).classes("justify-center")

    ui.add_css("""
    .editable-text {
        border-bottom: 1px solid #000 !important;
    }
    """)

    table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
    table.add_slot(
        "header",
        r"""
        <q-tr :props="props">
            <q-th auto-width />
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
        """,
    )
    table.add_slot(
        "body",
        r"""
        <q-tr :props="props">
            <q-td auto-width >
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                >
                    <q-tooltip>Delete</q-tooltip>
                </q-btn>
            </q-td>
            <q-td key="username" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.username" dense counter readonly />
                    <q-popup-edit v-model="props.row.username" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                </template>
                <template v-else>
                    {{ props.row.username }}
                </template>
            </q-td>
            <q-td key="password" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.password" type="password" dense counter readonly />
                    <q-popup-edit v-model="props.row.password" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" :type="props.row.password_visible ? 'text' : 'password'" dense autofocus counter @keyup.enter="scope.set">
                            <template v-slot:append>
                                <q-icon
                                    :name="props.row.password_visible ? 'visibility' : 'visibility_off'"
                                    class="cursor-pointer"
                                    @click="props.row.password_visible = !props.row.password_visible"
                                />
                            </template>
                        </q-input>
                    </q-popup-edit>
                </template>
                <template v-else>
                    <q-icon name="key" />
                </template>
            </q-td>
            <q-td key="domain" :props="props">
                <template v-if="props.row.is_editing">
                    <q-select v-model="props.row.domain" :options='"""
        + domain_options_json
        + r"""'
                        label="Choose a domain"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }" />
                </template>
                <template v-else>
                    {{ props.row.domain.label }}
                </template>
            </q-td>
            <q-td key="forward_to" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.forward_to" dense counter readonly />
                    <q-popup-edit v-model="props.row.forward_to" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                </template>
                <template v-else>
                    {{ props.row.forward_to }}
                </template>
            </q-td>
            <q-td key="status" :props="props">
                <template v-if="props.row.is_editing">
                    <q-select v-model="props.row.status" :options='"""
        + email_status_options_json
        + r"""'
                        label="Choose a status"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }" />
                </template>
                <template v-if="props.row.status.value === 1">
                    <q-btn size="sm" color="red" round dense icon="block" style="cursor: default;">
                        <q-tooltip>Blocked</q-tooltip>
                    </q-btn>
                </template>
            </q-td>
            <q-td key="description" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.description" dense counter readonly />
                    <q-popup-edit v-model="props.row.description" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                </template>
                <template v-else>
                    {{ props.row.description }}
                </template>
            </q-td>
            <q-td auto-width v-if="props.row.is_editing">
                <q-btn size="sm" color="blue" round dense icon="save"
                    @click="() => {{ $parent.$emit('save', props.row) }}"
                >
                    <q-tooltip>Save</q-tooltip>
                </q-btn>
            </q-td>
            <q-td auto-width v-if="!props.row.is_editing">
                <q-btn size="sm" color="black" round dense icon="edit"
                    @click="() => {{ $parent.$emit('edit', props.row) }}"
                >
                    <q-tooltip>Edit</q-tooltip
                </q-btn>
            </q-td>
        </q-tr>
        """,
    )
    table.on("update_ui_display", update_ui_display)
    table.on("delete", delete)
    table.on("save", save)
    table.on("edit", edit)
