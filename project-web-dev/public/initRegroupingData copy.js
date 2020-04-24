{
    "class": "go.GraphLinksModel",
        "nodeDataArray": [
            { "key": 1, "text": "Main 1", "isGroup": true, "category": "OfGroups" },
            { "key": 2, "text": "Main 2", "isGroup": true, "category": "OfGroups" },
            { "key": 3, "text": "Group A", "isGroup": true, "category": "OfNodes", "group": 1 },
            { "key": 4, "text": "Group B", "isGroup": true, "category": "OfNodes", "group": 1 },
            { "key": 5, "text": "Group C", "isGroup": true, "category": "OfNodes", "group": 2 },
            { "key": 6, "text": "Group D", "isGroup": true, "category": "OfNodes", "group": 2 },
            { "key": 7, "text": "Group E", "isGroup": true, "category": "OfNodes", "group": 6 },
            { "text": "first A", "group": 3, "key": -7 },
            { "text": "second A", "group": 3, "key": -8 },
            { "text": "first B", "group": 4, "key": -9 },
            { "text": "second B", "group": 4, "key": -10 },
            { "text": "third B", "group": 4, "key": -11 },
            { "text": "first C", "group": 5, "key": -12 },
            { "text": "second C", "group": 5, "key": -13 },
            { "text": "first D", "group": 6, "key": -14 },
            { "text": "first E", "group": 7, "key": -15 }
        ],
            "linkDataArray": [{ "from": 2, "to": 3 }, { "from": -13, "to": -15 }, { "from": -8, "to": -15 }]
}
