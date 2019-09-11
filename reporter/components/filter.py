import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import components.import_data as import_data
import components.admin as admin
import dash_bootstrap_components as dbc
import components.global_vars as global_vars

TABLE_PAGESIZE = 100


def format_selected_samples(filtered_df):
    "Returns a formatted string of selected samples"
    return "\n".join([row["name"] for index, row in filtered_df.iterrows()])


def html_collection_selector():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                dbc.Label(
                                    "Select Collection", html_for="collection-selector", className="m-0 font-weight-bold text-primary h6 d-block"),
                                className="card-header py-3"
                            ),
                            html.Div(
                                [
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup(
                                                [
                                                    dcc.Dropdown(
                                                        id="collection-selector",
                                                        value=None,
                                                    ),
                                                ]
                                            ),
                                        ], lg=9),
                                        dbc.Col([
                                            dbc.FormGroup(
                                                [
                                                    dcc.Link(
                                                        "Load collection",
                                                        id="collection-link",
                                                        href="/collection",
                                                        className="btn btn-primary"),
                                                ]
                                            )
                                        ], lg=3),
                                    ])
                                ],
                                className="card-body"
                            )
                        ], className="card shadow mb-4"
                    )
                ],
                className="col-lg-9"
            )

            # html.Div(id="tsv-download")
        ],
        className="row", id="collection-selector-div"
    )

#callback
def update_collection_button(collection, pathname):
    if pathname is None or pathname == "/":
        pathname = "/"
    path = pathname.split("/")
    if path[1] == "resequence-report":
        if collection is not None:
            return "/resequence-report/" + collection
        else:
            return "/resequence-report"
    else:
        if collection is not None:
            return "/collection/" + collection
        else:
            return "/collection"


def html_filter_drawer():
    qc_list_options = [
        {"label": "OK", "value": "pass:OK"},
        {"label": "Core Facility", "value": "fail:core facility"},
        {"label": "Supplying Lab", "value": "fail:supplying lab"},
        {"label": "Not checked", "value": "Not checked"}
    ]
    run_filter = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                html.H6(
                                    "Filter",
                                    className="m-0 font-weight-bold text-primary"
                                ),
                                className="card-header py-3"
                            ),
                            html.Div(
                                [
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.FormGroup(
                                                            [
                                                                dbc.Label(
                                                                    "Run", html_for="run-list"),
                                                                dcc.Dropdown(
                                                                    id="run-list",
                                                                    multi=True,
                                                                    value=[],
                                                                    placeholder="All runs selected",
                                                                ),
                                                            ]
                                                        ),
                                                        width=6, id="run-list-div"
                                                    ),
                                                    dbc.Col(
                                                        dbc.FormGroup(
                                                            [
                                                                dbc.Label(
                                                                    "Group", html_for="group-list"),
                                                                dcc.Dropdown(
                                                                    id="group-list",
                                                                    multi=True,
                                                                    value=[],
                                                                    placeholder="All groups selected",
                                                                ),
                                                            ]
                                                        ),
                                                        width=6,
                                                    ),
                                                ],
                                                form=True,
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.FormGroup(
                                                            [
                                                                html.Label(
                                                                    [
                                                                        "Species: "
                                                                    ],
                                                                    htmlFor="species-list",
                                                                    style={
                                                                        "display": "inline-block"}
                                                                ),
                                                                dcc.RadioItems(
                                                                    options=[
                                                                        {"label": "Provided",
                                                                         "value": "provided"},
                                                                        {"label": "Detected",
                                                                         "value": "detected"},
                                                                    ],
                                                                    value="provided",
                                                                    labelStyle={
                                                                        'margin': '0 0 0.5rem 0.5rem'},
                                                                    id="form-species-source",
                                                                    style={
                                                                        "display": "inline-block"}

                                                                ),
                                                                html.Div(
                                                                    dcc.Dropdown(
                                                                        id="species-list",
                                                                        multi=True,
                                                                        value=[],
                                                                        placeholder="All species selected",
                                                                    ),
                                                                    id="species-div"
                                                                )
                                                            ]
                                                        ),
                                                        width=6,
                                                    ),
                                                    dbc.Col(
                                                        dbc.FormGroup(
                                                            [
                                                                dbc.Label(
                                                                    "SSI QC", html_for="qc-list"),
                                                                dcc.Dropdown(
                                                                    id="qc-list",
                                                                    multi=True,
                                                                    options=qc_list_options,
                                                                    placeholder="All values selected",
                                                                    value=[]
                                                                ),
                                                            ]
                                                        ),
                                                        width=6,
                                                    ),
                                                ],
                                                form=True,
                                            ),
                                        ], width=9),
                                        dbc.Col([
                                            dbc.Row(dbc.Col([
                                                dbc.Label(["Sample names ", html.Span(
                                                    "(?)", id="sample-names-tooltip")],
                                                    html_for="samples-form",
                                                    style={"display": "block"}),
                                                dbc.Textarea(
                                                    id="samples-form",
                                                    placeholder="one sample per line",
                                                    value="",
                                                    rows=6
                                                ),
                                                dbc.Tooltip(
                                                    "Sample name must match exactly. "
                                                    "Search samples using regex by starting and finishing sample name with the '/' character.",
                                                    target="sample-names-tooltip",
                                                )
                                            ], width=12))
                                        ], width=3),
                                    ]),
                                    dbc.ButtonGroup([
                                        dbc.Button("Search samples",
                                                   id="apply-filter-button",
                                                   color="primary",
                                                   n_clicks=0),
                                        # dbc.Button("Generate download link (1000 samples max.)",
                                        #            id="generate-download-button",
                                        #            color="secondary",
                                        #            n_clicks=0)
                                    ]),
                                ],
                                className="card-body"
                            )
                        ], className="card shadow mb-4"
                    )
                ],
                className="col"
            )
            
            # html.Div(id="tsv-download")
        ],
        className="row"
    )

    return run_filter

def html_div_filter():
    qc_list_options = [
        {"label": "OK", "value": "pass:OK"},
        {"label": "Core Facility", "value": "fail:core facility"},
        {"label": "Supplying Lab", "value": "fail:supplying lab"},
        {"label": "Not checked", "value": "Not checked"}
    ]
    

    return html.Div([
        html.Div(
            [
                html.Div([
                    html.Div(
                        [
                            html.H6("List view",
                                className="m-0 font-weight-bold text-primary"),
                        ],
                        className="card-header py-3"
                    ),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    # dbc.Button("Remove selected",
                                    #            id="remove-selected",
                                    #            n_clicks=0,
                                    #            size="sm")
                                ]),
                            ], className="col-auto mr-auto"),
                            html.Div([

                                html.Span(
                                    "0", id="filter-sample-count"),
                                ' samples loaded.',

                                dbc.ButtonGroup([
                                    dbc.Button(html.I(className="fas fa-download fa-sm fa-fw"),
                                               id="generate-download-button",
                                               color="secondary",
                                               size="sm",
                                               className="ml-2",
                                               n_clicks=0)
                                ]),
                                html.Div(id="tsv-download")
                            ], className="col-auto"),
                        ], className="row mb-3"),
                        html.Div([], id="placeholder0"),
                        dash_table.DataTable(
                            data=[{}],
                            style_table={
                                'overflowX': 'scroll',
                            },
                            columns=global_vars.COLUMNS,
                            style_cell={
                                'width': '200px',
                                'padding': '0 15px'
                            },
                            style_cell_conditional=[
                                {
                                    "if": {"column_id": "ssi_stamper_failed_tests"},
                                    "textAlign": "left"
                                }
                            ],
                            fixed_rows={'headers': True},
                            # row_selectable='multi',
                            # filtering=True,  # Front end filtering
                            # sorting=True,
                            selected_rows=[],
                            # style_data_conditional=style_data_conditional,
                            # pagination_settings={
                            #     'current_page': 0,
                            #     'page_size': TABLE_PAGESIZE
                            # },
                            virtualization=False,
                            page_action='none',
                            id="datatable-ssi_stamper")
                    ], className="card-body bigtable")

                ], id="ssi_stamper-report", className="card shadow mb-4"),
            ]
        )
    ])


def generate_table(tests_df):
    qc_action = "properties.stamper.summary.stamp.value"
    if qc_action not in tests_df:
        tests_df[qc_action] = np.nan
    else:
        tests_df[qc_action] = tests_df[qc_action].str.split(":", expand=True)[1]

    r1_col = "properties.datafiles.summary.paired_reads"

    if r1_col not in tests_df:
        tests_df[r1_col] = np.nan

    values = {r1_col: ""}
    tests_df = tests_df.fillna(value=values)
    no_reads_mask = tests_df[r1_col] == ""
    tests_df.loc[no_reads_mask, qc_action] = "core facility (no reads)"
    mask = pd.isnull(tests_df[qc_action])
    tests_df.loc[mask, qc_action] = "not tested"
    slmask = tests_df[qc_action] == "supplying lab"
    tests_df.loc[slmask, qc_action] = "warning: supplying lab"

    # user_stamp_col = "stamp.supplying_lab_check.value"
    # # Overload user stamp to ssi_stamper
    # if user_stamp_col in tests_df.columns:
    #     user_OK_mask = tests_df[user_stamp_col] == "pass:OK"
    #     tests_df.loc[user_OK_mask, qc_action] = "*OK"
    #     user_sl_mask = tests_df[user_stamp_col] == "fail:supplying lab"
    #     tests_df.loc[user_sl_mask, qc_action] = "*warning: supplying lab"
    #     user_cf_mask = tests_df[user_stamp_col] == "fail:core facility"
    #     tests_df.loc[user_cf_mask, qc_action] = "*core facility"

    test_cols = [col for col in tests_df.columns if (col.startswith(
        "properties.stamper.summary."))]

    # Round columns:
    for col in global_vars.ROUND_COLUMNS:
        if col in tests_df.columns:
            tests_df[col] = round(tests_df[col], 3)

    def concatenate_failed(row):
        res = []
        tests = {}
        for col in test_cols:
            test_name = col.split(".")[-2]
            field = col.split(".")[-1]
            value = row[col]
            test = tests.get(test_name, {})
            test[field] = value
            tests[test_name] = test
        for testname in tests:
            test = tests[testname]
            if test["status"] == "fail":
                res.append("Test {}: {}, {}".format(
                    testname, test["status"], test["reason"]))
        row["ssi_stamper_failed_tests"] = ". ".join(res)
        return row

    tests_df = tests_df.apply(concatenate_failed, axis="columns")



    COLUMNS = global_vars.COLUMNS

    # Generate conditional formatting:
    style_data_conditional = []
    conditional_columns = ["properties.stamper.summary.stamp.value"]

    for status, color in ("fail", "#ea6153"), ("undefined", "#f1c40f"):
        style_data_conditional += list(map(lambda x: {"if": {
            "column_id": x, "filter": '{} eq "{}"'.format(x, status)}, "backgroundColor": color}, conditional_columns))

    for status, color in ("core facility", "#ea6153"), ("warning: supplying lab", "#f1c40f"):
        style_data_conditional += [{"if": {
            "column_id": qc_action, "filter": 'QC_action eq "{}"'.format(status)}, "backgroundColor": color}]

    tests_df["_id"] = tests_df["_id"].astype(str)

    tests_df = tests_df.filter([ c["id"] for c in COLUMNS])

    return tests_df


# callback
def filter_update_run_options(form_species, selected_collection):
    # Runs
    run_list = import_data.get_run_list()
    run_options = [
        {
            "label": "{} ({})".format(run["name"],
                                      len(run["samples"])),
            "value": run["name"]
        } for run in run_list]

    # Groups
    group_list = import_data.get_group_list(selected_collection)
    group_options = []
    for item in group_list:
        if pd.isnull(item["_id"]):
            group_options.append({
                "label": "Not defined ({})".format(item["count"]),
                "value": "Not defined"
            })
        else:
            group_options.append({
                "label": "{} ({})".format(item["_id"], item["count"]),
                "value": item["_id"]
            })

    species_list = import_data.get_species_list(
        form_species, selected_collection)

    species_options = []
    for item in species_list:
        if pd.isna(item["_id"]):
            species_options.append({
                "label": "Not classified",
                "value": "Not classified"
            })
        else:
            species_options.append({
                "label": item["_id"],
                "value": item["_id"]
            })
    return [run_options, run_options, group_options, species_options]


# callback
def filter_update_filter_values(param_store):
    runs = param_store.get("run", [])
    groups = param_store.get("group", [])
    species = param_store.get("species", [])
    qcs = param_store.get("qc", [])
    sample_names = param_store.get("sample_names", [])
    return [runs, groups, species, qcs, "\n".join(sample_names)]