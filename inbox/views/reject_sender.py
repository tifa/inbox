import logging

from nicegui import events, ui

from inbox.service.admin import (
    delete_reject_sender,
    list_reject_senders,
    upsert_reject_sender,
)
from inbox.views.notify import notify_error, notify_success

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


MASKED_PASSWORD = "*" * 10

def reject_sender():
    columns = [
        {
            "name": "username",
            "label": "Username",
            "field": "username",
            "sortable": True,
        },
        {
            "name": "domain_name",
            "label": "Domain",
            "field": "domain_name",
            "sortable": True,
        },
        {"name": "description", "label": "Description", "field": "description"},
    ]

    senders = list_reject_senders()

    rows = [
        {
            "id": sender.id,
            "username": sender.username,
            "domain_name": sender.domain_name,
            "description": sender.description,
        }
        for sender in senders
    ]

    def add_ui_row() -> None:
        new_id = max((dx["id"] for dx in rows), default=-1) + 1
        row = {
            "id": new_id,
            "username": "",
            "domain_name": "",
            "description": "",
            "is_editing": True,
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
            delete_reject_sender(e.args["id"])
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
                    upsert_reject_sender(
                        id=row["id"],
                        username=row["username"],
                        domain_name=row["domain_name"],
                        description=row["description"],
                    )
                    break
        except Exception as e:
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
        "Reject new sender", icon="add", color="accent", on_click=add_ui_row
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
            <q-td key="domain_name" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.domain_name" dense counter readonly />
                    <q-popup-edit v-model="props.row.domain_name" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                </template>
                <template v-else>
                    {{ props.row.domain_name }}
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
                />
            </q-td>
            <q-td auto-width v-if="!props.row.is_editing">
                <q-btn size="sm" color="black" round dense icon="edit"
                    @click="() => {{ $parent.$emit('edit', props.row) }}"
                />
            </q-td>
        </q-tr>
        """,
    )
    table.on("update_ui_display", update_ui_display)
    table.on("delete", delete)
    table.on("save", save)
    table.on("edit", edit)
