const gridStyles = {
    root: {
        flexGrow: 1,
        padding: '24px',
        backgroundColor: '#333',
    },
    paper: {
        border: 0,
        borderRadius: 3,
        color: 'white',
        padding: '10px 10px',
        textAlign: 'center',
        // backgroundColor: '#F1F1F1',
    },
};

const buttonStyles = {
    root: {
        color: "#fff",
        padding: "6px 16px",
        // fontSize: "0.875rem",
        minWidth: "64px",
        boxSizing: "border-box",
        transition: "background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,border 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms",
        fontFamily: "\Roboto\", \"Helvetica\", \"Arial\", sans-serif",
        fontWeight: "500",
        lineHeight: "1.75",
        borderRadius: "4px",
        letterSpacing: "0.02857em",
        // textTransform: "uppercase",
    },
    primary: {
        color: "rgba(0, 0, 0, 0.87)",
        backgroundColor: "#90caf9",
    },
    secondary: {
        color: "rgba(0, 0, 0, 0.87)",
        backgroundColor: "#f48fb1",
    },
    contained: {
        color: "rgba(0, 0, 0, 0.87)",
        boxShadow: "0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12)",
        backgroundColor: "#e0e0e0",
    },
    outlined: {
        border: "1px solid rgba(255, 255, 255, 0.23)",
        padding: "5px 15px",
    }
}


const innerStyles = {
    root: {
        flexGrow: 1,
        padding: '24px',
        backgroundColor: '#333',
    },
    title: {
        height: 48,
    },
    paper: {
        border: 0,
        borderRadius: 3,
        color: 'white',
        // height: 48,
        padding: '0 30px',
        textAlign: 'center',
        backgroundColor: '#424242',
    },
    warmPaper: {
        background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
        boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
    },
    coolPaper: {
        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
        boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
    }
}
export {
    gridStyles, buttonStyles, innerStyles
}