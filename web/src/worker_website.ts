import { log_data, get_json, get_html } from "./connector";
import { DEVMODE } from "./globals";
import { range, timer } from "./utils";

let main_text_area = $("#main_text_area")

export async function setup_intro_information() {
    main_text_area.html(await get_html("instructions.html"))
    await timer(10)
    $("#button_start").on("click", setup_main_question)
}

function next_main_question() {
    globalThis.data_i += 1;
    if (globalThis.data_i >= globalThis.data.length) {
        load_thankyou()
    } else {
        globalThis.data_now = globalThis.data[globalThis.data_i]
        setup_main_question()
    }
}

function tag_factory(tag) {
    return `<span class="tag_span">${tag}</span>`
}

async function setup_main_question() {
    globalThis.time_start = Date.now()

    let html = await get_html("main_task.html")
    html = html.replace("{{QUESTION}}", globalThis.data_now["question"])
    html = html.replace("{{ANSWER}}", globalThis.data_now["answer"])

    if (globalThis.data_now["mode"].includes("tags")) {
        html = html.replace("{{TAGS}}", globalThis.data_now["tags"].map((x) => tag_factory(x)).join(" "))
    } else {
        html = html.replace("{{TAGS}}", "")
    }

    if (globalThis.data_now["mode"].includes("blur")) {
        html = html.replace("{{POTENTIAL_BLURBOX}}", "<div class='paragraph_blurbox'></div>")
    } else {
        html = html.replace("{{POTENTIAL_BLURBOX}}", "")
    }
    main_text_area.html(html)
    await timer(10)

    $("#button_yes").on("click", () => {
        log_data(true)
        next_main_question()
    })
    $("#button_no").on("click", () => {
        log_data(false)
        next_main_question()
    })
}

async function load_thankyou() {
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