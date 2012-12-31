#!/bin/bash

# a q3-like (or yakuake-like) terminal for arbitrary applications.
#
# this lets a new monitor called "q3terminal" scroll in from the top into the
# current monitor. There the "scratchpad" will be shown (it will be created if
# it doesn't exist yet). If the monitor already exists it is scrolled out of
# the screen and removed again.
#
# Warning: this uses much resources because herbstclient is forked for each
# animation step.
#
# If a tag name is supplied, this is used instead of the scratchpad

tag="${1:-scratchpad}"

hc() {
    #echo "hc $@" >&2 ;
    herbstclient "$@" ;
}


hc add scratchpad


monitor=q3terminal

exists=false
if ! hc add_monitor $(printf "%dx%d%+d%+d" "${rect[@]}") \
                    "$tag" $monitor 2> /dev/null ; then
    exists=true
fi

update_geom() {
    local geom=$(printf "%dx%d%+d%+d" "${rect[@]}")
    hc move_monitor "$monitor" $geom
}

steps=5
interval=0.01

animate() {
    progress=( "$@" )
    for i in "${progress[@]}" ; do
        rect[3]=$((${y_line}-(i*termheight)/$steps))
        update_geom
        sleep "$interval"
    done
}

show() {

    mrect=( $(hc monitor_rect -p "" ) )
    termwidth=$(((${mrect[2]}*8)/10))
    termheight=400

    rect=(
        $termwidth
        $termheight
        $((${mrect[0]}+(${mrect[2]}-termwidth)/2))
        $((${mrect[1]}-termheight))
    )

    y_line=${mrect[1]}

    hc lock
    hc raise_monitor $monitor
    hc focus_monitor $monitor
    hc unlock
    hc lock_tag $monitor
    animate $(seq $steps -1 0)
}

hide() {
    rect=( $(hc monitor_rect "$monitor" ) )
    local tmp=${rect[0]}
    rect[0]=${rect[2]}
    rect[2]=${tmp}
    local tmp=${rect[1]}
    rect[1]=${rect[3]}
    rect[3]=${tmp}
    termheight=${rect[1]}
    y_line=${rect[3]} # height of the upper screen border

    animate $(seq 0 +1 $steps)
    hc remove_monitor $monitor
}

[ $exists = true ] && hide || show
