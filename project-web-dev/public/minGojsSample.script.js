var $ = go.GraphObject.make;  // for conciseness in defining templates

var myDiagram =
    $(go.Diagram, "myminDiv",  // create a Diagram for the DIV HTML element
        { // enable undo & redo
            "undoManager.isEnabled": true
        });

// define a simple Node template
myDiagram.nodeTemplate =
    $(go.Node, "Auto",  // the Shape will go around the TextBlock
        $(go.Shape, "RoundedRectangle",
            { strokeWidth: 0, fill: "white" },  // default fill is white
            // Shape.fill is bound to Node.data.color
            new go.Binding("fill", "color")),
        $(go.TextBlock,
            { margin: 8 },  // some room around the text
            // TextBlock.text is bound to Node.data.key
            new go.Binding("text", "key"))
    );

// but use the default Link template, by not setting Diagram.linkTemplate

// create the model data that will be represented by Nodes and Links
myDiagram.model = new go.GraphLinksModel(
    [
        { key: "Alpha", color: "lightblue" },
        { key: "Beta", color: "orange" },
        { key: "Gamma", color: "lightgreen" },
        { key: "Delta", color: "pink" }
    ],
    [
        { from: "Alpha", to: "Beta" },
        { from: "Alpha", to: "Gamma" },
        { from: "Beta", to: "Beta" },
        { from: "Gamma", to: "Delta" },
        { from: "Delta", to: "Alpha" }
    ]);