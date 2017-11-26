from .kt_tv_channel import *
import sqlite3
from datetime import date

def main():
    # connection
    db = sqlite3.connect('tv.db')
    cursor = db.cursor()
    
    # ready table
    try:
        cursor.execute('drop table schedules')
    except:
        pass


    cursor.execute('''
    create table schedules (
        ch       integer,
        ch_name  text,
        time     text,
        program  text
    )
    ''')

    today = date.today()    
    
    channels = get_all_channels()
    for ch, ch_name in channels:
        print('ch {}'.format(ch), end='')
        scheds = get_schedule(ch)
        for sched in scheds:
            cursor.execute('''
            insert into schedules values(
            ?,?,?,?
            )
            ''', (ch, ch_name, f'{today} {sched[0]:02}:{sched[1]:02}:00', sched[2] ))
        print('..done')
    cursor.close()
    db.commit()

if __name__ == '__main__':
    main()
