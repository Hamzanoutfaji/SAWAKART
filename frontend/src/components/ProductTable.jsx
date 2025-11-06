import { useState } from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import { FilterMatchMode } from "primereact/api";
import "primereact/resources/themes/saga-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import api from "../api";

export default function ProductTable({ products, onDelete }) {
  const [globalFilterValue, setGlobalFilterValue] = useState("");
  const [filters, setFilters] = useState({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    title: { value: null, matchMode: FilterMatchMode.CONTAINS },
    source: { value: null, matchMode: FilterMatchMode.CONTAINS },
    price: { value: null, matchMode: FilterMatchMode.CONTAINS },
    rating: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  const handleDelete = async (id) => {
    if (!confirm("Are you sure?")) return;
    await api.delete(`/products/${id}`);
    onDelete(id);
  };

  const onGlobalFilterChange = (e) => {
    const value = e.target.value;
    let _filters = { ...filters };
    _filters["global"].value = value;
    setFilters(_filters);
    setGlobalFilterValue(value);
  };

  const renderHeader = () => {
    return (
      <div className="flex justify-content-end">
        <span className="p-input-icon-left">
          <InputText
            value={globalFilterValue}
            onChange={onGlobalFilterChange}
            placeholder="Search products.."
          />
        </span>
      </div>
    );
  };

  // Template for clickable URL
  const urlBodyTemplate = (rowData) => (
    <a href={rowData.product_url} target="_blank" rel="noopener noreferrer">
      Link
    </a>
  );

  // Template for product image
  const imageBodyTemplate = (rowData) => (
    rowData.image_url ? (
      <img src={rowData.image_url} alt={rowData.title} style={{ width: "50px", height: "50px", objectFit: "contain" }} />
    ) : (
      "-"
    )
  );

  // Template for actions column
  const actionBodyTemplate = (rowData) => (
    <Button
      icon="pi pi-trash"
      className="p-button-danger p-button-sm"
      onClick={() => handleDelete(rowData.id)}
    />
  );

  const header = renderHeader();

  return (
    <div className="card p-3 shadow-sm mt-4">
      <h5 className="mb-3">Products List</h5>
      <DataTable
        value={products}
        responsiveLayout="scroll"
        stripedRows
        paginator
        rows={6}
        filters={filters}
        globalFilterFields={["title", "source", "price", "rating"]}
        header={header}
        emptyMessage="No products found."
      >
        <Column field="id" header="ID" sortable />
        <Column field="title" header="Title" sortable filter filterPlaceholder="Search by title" />
        <Column field="price" header="Price ($)" sortable filter filterPlaceholder="Search by price" />
        <Column field="rating" header="Rating" sortable filter filterPlaceholder="Search by rating" />
        <Column field="source" header="Source" sortable filter filterPlaceholder="Search by source" />
        <Column header="Image" body={imageBodyTemplate} />
        <Column header="URL" body={urlBodyTemplate} />
        <Column header="Actions" body={actionBodyTemplate} />
      </DataTable>
    </div>
  );
}