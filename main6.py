import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Exercise 8 – Charts and Tables"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    CATEGORIES = ["Food", "Transport", "Housing", "Other"]
    CATEGORY_COLORS = [
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.AMBER,
        ft.Colors.PINK,
    ]

    totals = {c: 0.0 for c in CATEGORIES}

    def build_pie_sections():
        total_sum = sum(totals.values())
        sections = []
        if total_sum <= 0:
            # Default "empty" chart
            for cat, color in zip(CATEGORIES, CATEGORY_COLORS):
                sections.append(
                    ft.PieChartSection(
                        value=1,
                        title=f"{cat}\n0.00 €",
                        title_style=ft.TextStyle(size=12, color=ft.Colors.WHITE),
                        color=color,
                        radius=70,
                    )
                )
            return sections
        
        for cat, color in zip(CATEGORIES, CATEGORY_COLORS):
            v = totals[cat]
            if v <= 0:
                continue
            percent = v / total_sum * 100
            sections.append(
                ft.PieChartSection(
                    value=v,
                    title=f"{cat}\n{percent:.1f}% ({v:.2f} €)",
                    title_style=ft.TextStyle(size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    color=color,
                    radius=80,
                )
            )
        return sections

    pie_chart = ft.PieChart(
        sections=build_pie_sections(),
        sections_space=3,
        center_space_radius=30,
        expand=True,
    )

    expenses_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Amount (€)")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_50,
        width=400, # Setting a width helps formatting in the column
    )

    category_dropdown = ft.Dropdown(
        label="Category (use this selector)",
        options=[ft.dropdown.Option(c) for c in CATEGORIES],
        value="Food",
        width=220,
    )

    def on_category_selected(e):
        category_dropdown.value = e.selection.value
        page.update()

    category_auto = ft.AutoComplete(
        suggestions=[
            ft.AutoCompleteSuggestion(key=c.lower(), value=c) for c in CATEGORIES
        ],
        on_select=on_category_selected,
    )

    amount_input = ft.TextField(
        label="Amount (€)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150,
    )

    error_text = ft.Text(color=ft.Colors.RED)

    def add_expense(e):
        error_text.value = ""
        cat = category_dropdown.value or "Food"
        try:
            amount = float(amount_input.value)
            if amount <= 0:
                raise ValueError()
        except Exception:
            error_text.value = "Enter a positive number."
            page.update()
            return
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        expenses_table.rows.append(
            ft.DataRow(
                [
                    ft.DataCell(ft.Text(date_str)),
                    ft.DataCell(ft.Text(cat)),
                    ft.DataCell(ft.Text(f"{amount:.2f}")),
                ]
            )
        )
        totals[cat] += amount
        pie_chart.sections = build_pie_sections()
        amount_input.value = ""
        expenses_table.update()
        pie_chart.update()
        page.update()

    add_button = ft.ElevatedButton("Add expense", on_click=add_expense)

    # --- LAYOUT DEFINITIONS ---

    # 1. Left Side: The Form and the Table
    left_column = ft.Column(
        controls=[
            ft.Text("Category (autocomplete):"),
            category_auto,
            category_dropdown,
            amount_input,
            add_button,
            error_text,
            ft.Divider(),
            ft.Text("All expense entries:", weight=ft.FontWeight.BOLD),
            expenses_table,
        ],
        scroll=ft.ScrollMode.AUTO, # Allows scrolling if the list gets long
        expand=True,               # Take up 50% of the width
    )

    # 2. Right Side: The Chart
    right_column = ft.Column(
        controls=[
            ft.Text("Share of expenses by category:", size=18, weight=ft.FontWeight.BOLD),
            pie_chart
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,               # Take up the other 50% of the width
    )

    # 3. Add the main structure to the page
    page.add(
        ft.Text("Daily expenses in 4 categories", size=22, weight=ft.FontWeight.BOLD),
        ft.Text(
            "You can type category in autocomplete or select it from the dropdown, then enter amount and click 'Add expense'."
        ),
        ft.Divider(),
        # The Main Row holding Left and Right columns
        ft.Row(
            controls=[
                left_column,
                ft.VerticalDivider(width=1), # Adds a faint line between columns
                right_column
            ],
            expand=True, # Expand the row to fill the page height
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )

ft.app(main)