// Base path to portfolio assets (keep leading ./ so paths resolve from page)
const ASSETS_BASE = "./assets/portfolio/";
const INDEX_PATH = ASSETS_BASE + "index.json";

const TOML_PARSER = (typeof TOML !== "undefined" ? TOML : (typeof toml !== "undefined" ? toml : undefined));
const JSON_FILE_NAME = "item.json";

async function loadPortfolioItems() {
    const container = document.getElementById("portfolio-items");
    if (!container) {
        return;
    }

    try {
        const folders = await get_index();
        if (!Array.isArray(folders)) {
            throw new Error("index.json must be an array of folder names");
        }
        const items = [];

        for (const folder of folders) {
            const data = await get_json_for_folder(folder);

            if (!data) {
                // skip this folder if we couldn't parse any metadata
                continue;
            }
            data.folder = folder;
            items.push(data);
        }
        
        if (items.length === 0) {
            container.textContent = "No portfolio items found.";
            return;
        }
        
        const list = document.createElement("div");
        list.className = "portfolio-list";
        
        for (const item of items) {
            const card = document.createElement("article");
            card.className = "portfolio-card";
            
            const title = document.createElement("h3");
            title.textContent = item.title || "Untitled";
            
            const meta = document.createElement("p");
            const grade = Array.isArray(item.grade) ? item.grade.join(", ") : item.grade || "";
            meta.textContent = [item.school, item.curriculum, grade, item.subject]
            .filter(Boolean)
            .join(" • ");
            
            const type = document.createElement("p");
            type.textContent = item.item_type ? `Type: ${item.item_type}` : "";
            
            const resources = document.createElement("ul");
            if (Array.isArray(item.resources)) {
                for (const resource of item.resources) {
                    const li = document.createElement("li");
                    if (resource.url) {
                        li.innerHTML = `<a href="${resource.url}" target="_blank" rel="noopener">${resource.label || resource.url}</a>`;
                    } else if (resource.path) {
                        li.innerHTML = `<a href="${ASSETS_BASE}${item.folder}/${resource.path}">${resource.label || resource.path}</a>`;
                    } else {
                        li.textContent = resource.label || "Resource";
                    }
                    resources.appendChild(li);
                }
            }
            
            if (resources.children.length === 0) {
                const empty = document.createElement("p");
                empty.textContent = "Resources coming soon.";
                card.appendChild(title);
                card.appendChild(meta);
                if (type.textContent) {
                    card.appendChild(type);
                }
                card.appendChild(empty);
            } else {
                card.appendChild(title);
                card.appendChild(meta);
                if (type.textContent) {
                    card.appendChild(type);
                }
                card.appendChild(resources);
            }
            
            list.appendChild(card);
        }
        
        container.innerHTML = "";
        container.appendChild(list);
    } catch (error) {
        console.error(error);
        container.textContent = "Error loading portfolio: " + (error && error.message ? error.message : String(error));
        return;
    }
}

async function get_index() {
    const response = await fetch(INDEX_PATH);
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();
}

async function get_json_for_folder(folder) {
    const itemTomlUrl = `${ASSETS_BASE}${folder}/${JSON_FILE_NAME}`;
    const itemResponse = await fetch(itemTomlUrl);
    if (!itemResponse.ok) {
        throw new Error(`Toml parsing error: ${itemResponse.status}`);
    }
    return await itemResponse.json();
}

document.addEventListener("DOMContentLoaded", loadPortfolioItems);
