import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
    name: "CustomUtils.CounterWithReset",
    async setup() {
        // Python側からのイベント "counter_node_reset_trigger" を待ち受ける
        api.addEventListener("counter_node_reset_trigger", (event) => {
            const targetNodeId = event.detail.node_id;
            
            // 現在のグラフから対象のノードを探す
            const node = app.graph.getNodeById(targetNodeId);
            if (node && node.widgets) {
                // "reset_switch" という名前のウィジェットを探す
                const switchWidget = node.widgets.find(w => w.name === "reset_switch");
                if (switchWidget) {
                    // 値を強制的に false (オフ) に書き換える
                    switchWidget.value = false;
                    
                    // 画面の再描画を要求
                    node.setDirtyCanvas(true, true);
                }
            }
        });
    }
});