const show_menu = () => {
    let side_bar = $('.side__bar')
    side_bar.css({"display":"block"})

    let menu = $(".open__button")
    menu.css({"display":"none"})

}

const hide_menu = () => {
    let element = $('.side__bar')
    element.css({"display":"none"})

    let menu = $(".open__button")
    menu.css({"display":"block"})
}
