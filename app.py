import streamlit as st
import pandas as pd
from dateutil.parser import parse
from datetime import timedelta

def clean_date(date: str):
    if "→" in date:
        start_date, end_date = date.split("→")
        start = clean_date(start_date)
        end = clean_date(end_date)
        return pd.Series({
            "Start Time": start["Start Time"],
            "Start Date": start["Start Date"],
            "End Time": end["End Time"],
            "End Date": end["End Date"]
        })

    if ":" in date:
        # We know there is a time involved

        if "-" in date:
            start, end  = date.split("-")
            start = parse(start)
            end = parse(end)
        else:
            start = parse(date)
            end = start + timedelta(hours=1)

        start_time = start.strftime("%H:%M:%S")
        start_date = end_date = start.strftime("%y/%m/%d")
        end_time = end.strftime("%H:%M:%S")
    else:
        # supply a default start and end time to fill the entire day
        start_time = "00:00:00"
        end_time = "23:59:59"
        start_date = end_date = parse(date).strftime("%y/%m/%d")

    return pd.Series({
            "Start Time": start_time,
            "Start Date": start_date,
            "End Time": end_time,
            "End Date": end_date
        })

"# Notion Calendar CSV Cleaner for Outlook"

file = st.file_uploader(label="CSV from Notion")

if file:
    df = pd.read_csv(file)

    # calculate date columns for Outlook
    dates = df.Date.apply(clean_date)

    # clean up dateframe to merge
    df.drop("Date", inplace=True, axis=1)
    df.rename(columns={
        "Name": "Subject", 
        "Shoes": "Description"
        }, inplace=True)
    
    # join date
    final = pd.concat([df, dates], axis=1)

    # provide download button
    st.download_button("Download CSV file from Outlook import", final.to_csv(index=False), 
            file_name="Notion-to-Outlook-RinceNaLeon.csv",
            mime="text/csv")