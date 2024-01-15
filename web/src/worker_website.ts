import { log_data, get_json, get_html } from "./connector";
import { DEVMODE } from "./globals";
import { range, timer } from "./utils";

let main_text_area = $("#main_text_area")

export async function setup_intro_information() {
    main_text_area.html(await get_html("instructions.html"))
    // hack for event loop
    await 10
    $("#button_start").on("click", setup_main_questions)
}

async function setup_main_questions() {
    console.log("Main questions", globalThis.data_now)
    return
    let article = globalThis.data_now["article"]

    let frame_obj = $(`<div id="article_frame">${article}</div>`)
    let question_obj = $('<div id="main_question_panel"></div>')
    main_text_area.html("")
    main_text_area.append(frame_obj)
    main_text_area.append(question_obj)
    main_text_area.scrollTop(0)

    // hack for JS event loop
    await timer(10)
}

async function load_thankyou() {
    // log last phase
    globalThis.phase += 1;
    log_data()

    main_text_area.html("Please wait 3s for data synchronization to finish.")
    await timer(1000)
    main_text_area.html("Please wait 2s for data synchronization to finish.")
    await timer(1000)
    main_text_area.html("Please wait 1s for data synchronization to finish.")
    await timer(1000)

    let html_text = `Thank you for participating in our study. For any further questions about this project or your data, <a href="mailto:vilem.zouhar@inf.ethz.ch">send us a message</a>.`;
    console.log("PID", globalThis.prolific_pid)
    if (globalThis.prolific_pid != null) {
        html_text += `<br>Please click <a href="https://app.prolific.com/submissions/complete?cc=C693YF4X">this link</a> to go back to Prolific. `
        html_text += `Alternatively use this code <em>C693YF4X</em>.`
    }
    main_text_area.html(html_text);
}