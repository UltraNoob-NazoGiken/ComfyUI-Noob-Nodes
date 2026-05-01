import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

console.log("★★★ Noob-Nodes: JS Initializing ★★★");

app.registerExtension({
    name: "NoobNodes.SimpleTextDisplay",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "SimpleTextDisplay") {
            
            // ノード作成時のフック
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // 表示用のHTML要素を作成
                const container = document.createElement("div");
                container.style.color = "#00ffcc";
                container.style.background = "rgba(0,0,0,0.8)";
                container.style.padding = "10px";
                container.style.marginTop = "10px";
                container.style.borderRadius = "4px";
                container.style.border = "1px solid #00ffcc";
                container.style.minHeight = "30px";
                container.innerText = "Waiting for Python message...";

                // widgetとして追加（SAM3等でも使われる手法）
                this.addDOMWidget("noob_display", "display", container);
                
                // ノードのサイズを更新
                this.onResize?.(this.size);
                
                return r;
            };

            // Python側 (PromptServer) からのメッセージ待受
            api.addEventListener("noob-text-update", (event) => {
                console.log("★★★ Message Received! ★★★", event.detail);
                const { node_id, text } = event.detail;
                
                // 画面上の全ノードから対象を探す（app.graph._nodesを使用）
                const nodes = app.graph._nodes.filter(n => n.type === "SimpleTextDisplay");
                for (const n of nodes) {
                    // 追加したDOMウィジェットを探して更新
                    const w = n.widgets?.find(w => w.name === "noob_display");
                    if (w && w.element) {
                        w.element.innerText = text;
                        n.setDirtyCanvas(true, true);
                    }
                }
            });
        }
    }
});