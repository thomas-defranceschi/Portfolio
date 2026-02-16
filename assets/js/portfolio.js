const INDEX_PATH = "./assets/portfolio/index.json";

async function loadPortfolioItems() {
    const container = document.getElementById("portfolio-items");
    if (!container) {
        return;
    }

    try {
        const folders = await get_index();
        container.textContent = "Index loaded succesfully"
        const items = [];

        for (const folder of folders) {
            const itemResponse = await fetch(`assets/portfolio/${folder}/item.toml`);
            if (!itemResponse.ok) {
                continue;
            }

            const tomlText = await itemResponse.text();
            const data = TOML.parse(tomlText);
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
                        li.innerHTML = `<a href="assets/portfolio/${item.folder}/${resource.path}">${resource.label || resource.path}</a>`;
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
        container.textContent += error;
    }

    async function get_index() {
        const response = await fetch(INDEX_PATH);
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    }

}

document.addEventListener("DOMContentLoaded", loadPortfolioItems);
