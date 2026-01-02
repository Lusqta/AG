
import os

content = r"""{% extends 'sales/base.html' %}

{% block content %}
<div class="header">
    <h2 style="font-size: 1.75rem; font-weight: 700;">Histórico de Vendas</h2>
    <div>
        <a href="{% url 'export_sales_report' %}" class="btn btn-secondary" style="margin-right: 0.5rem;"><i
                class="fas fa-file-excel"></i> Exportar</a>
        <a href="{% url 'create_sale' %}" class="btn btn-primary">+ Nova Venda</a>
    </div>
</div>


<!-- Filter Form -->
<div class="card" style="margin-bottom: 1.5rem;">
    <form method="get"
        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; align-items: end;">
        <div>
            <label
                style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #64748b;">Buscar</label>
            <input type="text" name="search" value="{{ search_query }}" placeholder="Cliente, Veículo..."
                style="width: 100%; padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.9rem;">
        </div>
        <div>
            <label
                style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #64748b;">De</label>
            <input type="date" name="date_min" value="{{ date_min }}"
                style="width: 100%; padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.9rem;">
        </div>
        <div>
            <label
                style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #64748b;">Até</label>
            <input type="date" name="date_max" value="{{ date_max }}"
                style="width: 100%; padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.9rem;">
        </div>
        <div>
            <label
                style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #64748b;">Vendedor</label>
            <select name="salesperson"
                style="width: 100%; padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.9rem; background-color: white;">
                <option value="">Todos</option>
                {% for u in users %}
                <option value="{{ u.id }}" {% if selected_salesperson == u.id %}selected{% endif %}>{{ u.username }}</option>
                {% endfor %}
            </select>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <button type="submit" class="btn btn-primary"
                style="flex: 1; padding: 0.6rem; font-size: 0.9rem;">Filtrar</button>
            {% if search_query or date_min or date_max or selected_salesperson %}
            <a href="{% url 'sale_list' %}" class="btn btn-secondary"
                style="padding: 0.6rem; display: flex; align-items: center; justify-content: center;"
                title="Limpar Filtros">
                <i class="fas fa-times"></i>
            </a>
            {% endif %}
        </div>
    </form>
</div>

<div class="card">
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Veículo</th>
                    <th>Cliente</th>
                    <th>Vendedor</th>
                    <th>Preço de Venda</th>
                </tr>
            </thead>
            <tbody>
                {% for sale in sales %}
                <tr>
                    <td>{{ sale.sale_date|date:"d/m/Y" }}</td>
                    <td style="font-weight: 500;">{{ sale.vehicle }}</td>
                    <td><a href="{% url 'customer_detail' sale.customer.pk %}"
                            style="color: var(--secondary-color); font-weight: 500;">{{ sale.customer }}</a></td>
                    <td>{{ sale.salesperson.get_full_name|default:sale.salesperson.username }}</td>
                    <td style="font-weight: 600; color: var(--success-color);">R$ {{ sale.sale_price|floatformat:2 }}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" style="text-align: center; padding: 2rem;">Nenhuma venda registrada.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""

file_path = r"c:\Users\Lucas\Downloads\AG\sales\templates\sales\sale_list.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully wrote to {file_path}")
