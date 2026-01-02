
import os

content = """{% extends 'sales/base.html' %}

{% block content %}
<div class="header">
    <h2 style="font-size: 1.75rem; font-weight: 700;">{{ customer.first_name }} {{ customer.last_name }}</h2>
    <div>
        <span class="badge badge-{{ customer.status }}" style="font-size: 1rem; margin-right: 1rem;">{{ customer.get_status_display }}</span>
        <button class="btn btn-secondary" onclick="alert('Funcionalidade de editar em breve (use Admin)')">Editar</button>
        {% if request.user.is_superuser or "Gerentes" in request.user.groups.all.0.name %}
        <a href="{% url 'customer_delete' customer.pk %}" class="btn" style="background-color: #fee2e2; color: #991b1b; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block;">Apagar</a>
        {% endif %}
    </div>
</div>

<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
    <!-- Customer Info -->
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">Informações de Contato</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
                <label>E-mail</label>
                <p>{{ customer.email }}</p>
            </div>
            <div>
                <label>Telefone</label>
                <p>{{ customer.phone }}</p>
            </div>
            <div style="grid-column: 1 / -1;">
                <label>Endereço</label>
                <p>{{ customer.address|default:"Não informado" }}</p>
            </div>
            <div>
                <label>Atribuído a</label>
                <p>{{ customer.assigned_to.get_full_name|default:customer.assigned_to.username|default:"Não atribuído" }}</p>
            </div>
            <div>
                <label>Última Atualização</label>
                <p>{{ customer.created_at|date:"d/m/Y" }}</p>
            </div>
        </div>
    </div>

    <!-- Purchase History -->
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">Histórico de Compras</h3>
        {% if customer.purchases.exists %}
        <ul style="list-style: none;">
            {% for purchase in customer.purchases.all %}
            <li style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #f1f5f9;">
                <div style="font-weight: 600;">{{ purchase.vehicle }}</div>
                <div style="color: #64748b; font-size: 0.875rem;">{{ purchase.sale_date|date:"d/m/Y" }} • R$ {{ purchase.sale_price }}</div>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p style="color: #94a3b8; font-style: italic;">Nenhuma compra registrada.</p>
        {% endif %}
    </div>
</div>
{% endblock %}
"""

file_path = r"c:\Users\Lucas\Downloads\AG\sales\templates\sales\customer_detail.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully wrote to {file_path}")
