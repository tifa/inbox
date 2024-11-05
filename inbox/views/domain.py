import logging

from nicegui import events, ui

from inbox.service.admin import delete_domain, list_domains, upsert_domain
from inbox.views.notify import notify_error, notify_success

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def domain():
    columns = [
        {"name": "num_emails", "label": "# Emails", "field": "num_emails"},
        {"name": "name", "label": "Domain", "field": "name", "sortable": True},
        {"name": "description", "label": "Description", "field": "description"},
    ]

    domains = list_domains()
    rows = []
    for domain in domains:
        has_catch_all = any(email.username == "" for email in domain.emails)
        rows.append(
        {
            "id": domain.id,
            "name": domain.name,
            "num_emails": (
                f"{len(domain.emails)} / ∞" if has_catch_all else len(domain.emails)
            ),
            "description": domain.description,
        })

    def add_ui_row() -> None:
        new_id = max((dx["id"] for dx in rows), default=-1) + 1
        row = {
            "id": new_id,
            "name": "",
            "num_emails": 0,
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
            delete_domain(e.args["id"])
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
                    upsert_domain(
                        id=row["id"],
                        name=row["name"],
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

    ui.button("Add domain", icon="add", color="accent", on_click=add_ui_row).classes(
        "justify-center"
    )

    ui.add_css("""
    .editable-text {
        border-bottom: 1px solid #000 !important;
    }
    """)

    table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
    # fmt: off
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
                <template v-if="props.row.num_emails == 0">
                    <q-btn size="sm" color="warning" round dense icon="delete"
                        @click="() => $parent.$emit('delete', props.row)"
                    >
                        <q-tooltip>Delete</q-tooltip>
                    </q-btn>
                </template>
            </q-td>
            <q-td key="num_emails" :props="props">
                <template v-if="!props.row.is_editing">
                    {{ props.row.num_emails }}
                </template>
            </q-td>
            <q-td key="name" :props="props">
                <template v-if="props.row.is_editing">
                    <q-input v-model="props.row.name" dense counter readonly />
                    <q-popup-edit v-model="props.row.name" v-slot="scope"
                        @update:model-value="() => { $parent.$emit('update_ui_display', props.row) }"
                    >
                        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                </template>
                <template v-else>
                    {{ props.row.name }}
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
                    <q-tooltip>Edit</q-tooltip>
                </q-btn>
            </q-td>
        </q-tr>
        """,
    )
    # fmt: on
    table.on("update_ui_display", update_ui_display)
    table.on("delete", delete)
    table.on("save", save)
    table.on("edit", edit)
