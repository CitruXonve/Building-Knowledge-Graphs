export default class regroupingController {

    static init = (ViewerId, data, onChange, isPaletteOn) => {
        if (window.goSamples) goSamples();  // init for these samples -- you don't need to call this
        var $ = go.GraphObject.make;

        var myDiagram =
            $(go.Diagram, ViewerId,
                {
                    // what to do when a drag-drop occurs in the Diagram's background
                    mouseDrop: function (e) { finishDrop(e, null); },
                    layout:  // Diagram has simple horizontal layout
                        $(go.GridLayout,
                            { wrappingWidth: Infinity, alignment: go.GridLayout.Position, cellSize: new go.Size(1, 1) }),
                    "commandHandler.archetypeGroupData": { isGroup: true, category: "OfNodes" },
                    "undoManager.isEnabled": true
                });

        // There are two templates for Groups, "OfGroups" and "OfNodes".

        // this function is used to highlight a Group that the selection may be dropped into
        function highlightGroup(e, grp, show) {
            if (!grp) return;
            e.handled = true;
            if (show) {
                // cannot depend on the grp.diagram.selection in the case of external drag-and-drops;
                // instead depend on the DraggingTool.draggedParts or .copiedParts
                var tool = grp.diagram.toolManager.draggingTool;
                var map = tool.draggedParts || tool.copiedParts;  // this is a Map
                // now we can check to see if the Group will accept membership of the dragged Parts
                if (grp.canAddMembers(map.toKeySet())) {
                    grp.isHighlighted = true;
                    return;
                }
            }
            grp.isHighlighted = false;
        }

        // Upon a drop onto a Group, we try to add the selection as members of the Group.
        // Upon a drop onto the background, or onto a top-level Node, make selection top-level.
        // If this is OK, we're done; otherwise we cancel the operation to rollback everything.
        function finishDrop(e, grp) {
            var ok = (grp !== null
                ? grp.addMembers(grp.diagram.selection, true)
                : e.diagram.commandHandler.addTopLevelParts(e.diagram.selection, true));
            if (!ok) e.diagram.currentTool.doCancel();
        }

        myDiagram.groupTemplateMap.add("OfGroups",
            $(go.Group, "Auto",
                {
                    background: "transparent",
                    // highlight when dragging into the Group
                    mouseDragEnter: function (e, grp, prev) { highlightGroup(e, grp, true); },
                    mouseDragLeave: function (e, grp, next) { highlightGroup(e, grp, false); },
                    computesBoundsAfterDrag: true,
                    // when the selection is dropped into a Group, add the selected Parts into that Group;
                    // if it fails, cancel the tool, rolling back any changes
                    mouseDrop: finishDrop,
                    handlesDragDropForMembers: true,  // don't need to define handlers on member Nodes and Links
                    // Groups containing Groups lay out their members horizontally
                    layout:
                        $(go.GridLayout,
                            {
                                wrappingWidth: Infinity, alignment: go.GridLayout.Position,
                                cellSize: new go.Size(1, 1), spacing: new go.Size(4, 4)
                            })
                },
                new go.Binding("background", "isHighlighted", function (h) { return h ? "rgba(255,0,0,0.2)" : "transparent"; }).ofObject(),
                $(go.Shape, "Rectangle",
                    { fill: null, stroke: "#FFDD33", strokeWidth: 2 }),
                $(go.Panel, "Vertical",  // title above Placeholder
                    $(go.Panel, "Horizontal",  // button next to TextBlock
                        { stretch: go.GraphObject.Horizontal, background: "#FFDD33" },
                        $("SubGraphExpanderButton",
                            { alignment: go.Spot.Right, margin: 5 }),
                        $(go.TextBlock,
                            {
                                alignment: go.Spot.Left,
                                editable: true,
                                margin: 5,
                                font: "bold 18px sans-serif",
                                opacity: 0.75,
                                stroke: "#404040"
                            },
                            new go.Binding("text", "text", t => t.match(/^\s*note|^\s*\*/ig)? null : t.length > 40? t.substring(0, 40)+'...' : t).makeTwoWay()) //t => {t.length > 16 ? t.substring(0, 16)+'...' : t} 
                    ),  // end Horizontal Panel
                    $(go.Placeholder,
                        { padding: 5, alignment: go.Spot.TopLeft })
                )  // end Vertical Panel
            ));  // end Group and call to add to template Map

        myDiagram.groupTemplateMap.add("OfNodes",
            $(go.Group, "Auto",
                {
                    background: "transparent",
                    ungroupable: true,
                    // highlight when dragging into the Group
                    mouseDragEnter: function (e, grp, prev) { highlightGroup(e, grp, true); },
                    mouseDragLeave: function (e, grp, next) { highlightGroup(e, grp, false); },
                    computesBoundsAfterDrag: true,
                    // when the selection is dropped into a Group, add the selected Parts into that Group;
                    // if it fails, cancel the tool, rolling back any changes
                    mouseDrop: finishDrop,
                    handlesDragDropForMembers: true,  // don't need to define handlers on member Nodes and Links
                    // Groups containing Nodes lay out their members vertically
                    layout:
                        $(go.GridLayout,
                            {
                                wrappingColumn: 1, alignment: go.GridLayout.Position,
                                cellSize: new go.Size(1, 1), spacing: new go.Size(4, 4)
                            })
                },
                new go.Binding("background", "isHighlighted", function (h) { return h ? "rgba(255,0,0,0.2)" : "transparent"; }).ofObject(),
                $(go.Shape, "Rectangle",
                    { fill: null, stroke: "#33D3E5", strokeWidth: 2 }),
                $(go.Panel, "Vertical",  // title above Placeholder
                    $(go.Panel, "Horizontal",  // button next to TextBlock
                        { stretch: go.GraphObject.Horizontal, background: "#33D3E5" },
                        $("SubGraphExpanderButton",
                            { alignment: go.Spot.Right, margin: 5 }),
                        $(go.TextBlock,
                            {
                                alignment: go.Spot.Left,
                                editable: true,
                                margin: 5,
                                font: "bold 16px sans-serif",
                                opacity: 0.75,
                                stroke: "#404040"
                            },
                            new go.Binding("text", "text", t => t.match(/^\s*note|^\s*\*/ig)? null : t.length > 16? t.substring(0, 8)+'...'+t.substring(t.length-8) : t).makeTwoWay())
                    ),  // end Horizontal Panel
                    $(go.Placeholder,
                        { padding: 5, alignment: go.Spot.TopLeft })
                )  // end Vertical Panel
            ));  // end Group and call to add to template Map

        myDiagram.nodeTemplate =
            $(go.Node, "Auto",
                { // dropping on a Node is the same as dropping on its containing Group, even if it's top-level
                    mouseDrop: function (e, nod) { finishDrop(e, nod.containingGroup); }
                },
                $(go.Shape, "Rectangle",
                    { fill: "#ACE600", stroke: null },
                    new go.Binding("fill", "color")),
                $(go.TextBlock,
                    {
                        margin: 5,
                        editable: true,
                        font: "bold 13px sans-serif",
                        opacity: 0.75,
                        stroke: "#404040"
                    },
                    new go.Binding("text", "text", t => t.match(/^\s*note|^\s*\*/ig)? null :  t.length > 16? t.substring(0, 8)+'...'+t.substring(t.length-8) : t).makeTwoWay())
            );

        // myDiagram.addModelChangedListener(function(evt) {
        //     if (evt.isTransactionFinished) saveModel(evt.model);
        //     });
        myDiagram.addModelChangedListener(onChange);

        // initialize the Palette and its contents
        var myPalette = isPaletteOn ?
            $(go.Palette, "myPaletteDiv",
                {
                    nodeTemplateMap: myDiagram.nodeTemplateMap,
                    groupTemplateMap: myDiagram.groupTemplateMap,
                    layout: $(go.GridLayout, { wrappingColumn: 1, alignment: go.GridLayout.Position })
                }) : {};
        myPalette.model = new go.GraphLinksModel([
            { text: "lightgreen", color: "#ACE600" },
            { text: "yellow", color: "#FFDD33" },
            { text: "lightblue", color: "#33D3E5" }
        ]);

        // var slider = document.getElementById("levelSlider");
        // slider.addEventListener('change', reexpand);
        // slider.addEventListener('input', reexpand);

        this.load(myDiagram, data);
        return myDiagram;
    }

    expandGroups(g, i, level) {
        if (!(g instanceof go.Group)) return;
        g.isSubGraphExpanded = i < level;
        g.memberParts.each(function (m) {
            expandGroups(m, i + 1, level);
        })
    }
    reexpand(e, myDiagram) {
        myDiagram.startTransaction("reexpand");
        var level = parseInt(document.getElementById("levelSlider").value);
        myDiagram.findTopLevelGroups().each(function (g) { expandGroups(g, 0, level); })
        myDiagram.commitTransaction("reexpand");
    }

    // save a model to and load a model from JSON text, displayed below the Diagram
    // static save(myDiagram, id) { //default id: "mySavedModel"
    //     document.getElementById(id).value = myDiagram.model.toJson();
    //     myDiagram.isModified = false;
    // }
    // static load(myDiagram, id) {
    //     myDiagram.model = go.Model.fromJson(document.getElementById(id).value);
    // }
    static extract(myDiagram) {
        return myDiagram.model.toJson();
    }
    static load(myDiagram, data) {
        myDiagram.model = go.Model.fromJson(data);
    }
}