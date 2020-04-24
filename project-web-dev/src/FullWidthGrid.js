import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';


export default function FullWidthGrid() {
  const styles = {
    root: {
      flexGrow: 1,
      padding: '24px', 
      backgroundColor: '#333',
    },
    paper: {
      border: 0,
      borderRadius: 3,
      color: 'white',
      height: 48,
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

  return (
    <div style={styles.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper style={styles.paper}>xs=12</Paper>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Paper style={{...styles.paper, ...styles.warmPaper}}>xs=12 sm=6</Paper>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Paper style={{...styles.paper, ...styles.coolPaper}}>xs=12 sm=6</Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper style={styles.paper}>xs=6 sm=3</Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper style={styles.paper}>xs=6 sm=3</Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper style={styles.paper}>xs=6 sm=3</Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper style={styles.paper}>xs=6 sm=3</Paper>
        </Grid>
      </Grid>
    </div>
  );
}
