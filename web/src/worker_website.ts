import { log_data, get_json, get_html } from "./connector";
import { DEVMODE } from "./globals";
import { timer } from "./utils";

let main_text_area = $("#main_text_area")

export async function setup_intro_information_1() {
    main_text_area.html(await get_html("instructions_1.html"))
    await timer(10)
    $("#button_start").on("click", setup_intro_information_2)
}

export async function setup_intro_information_2() {
    main_text_area.html(await get_html("instructions_2.html"))
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

async function show_evaluation(response: Boolean) {
    let correct = globalThis.data_now["correct"]
    let html = await get_html("modal_response.html")
    let text_correct = "<span class='span_correct'>correct</span>"
    let text_incorrect = "<span class='span_incorrect'>incorrect</span>"
    let message = ""
    if (!globalThis.data_now["reveal"]) {
        message = `You answered that the AI was ${response ? text_correct : text_incorrect}.<br>Please continue paying attention.`
    } else {
        if (response == correct) {
            message = `You answered that the AI was ${response ? text_correct : text_incorrect} and the AI was in fact ${correct ? text_correct : text_incorrect}`
        } else {
            message = `You answered that the AI was ${response ? text_correct : text_incorrect} but the AI was in fact ${correct ? text_correct : text_incorrect}`
        }
    }

    // compute reward
    let gain = 0
    if (correct == response) {
        gain += 3;
        message += `<br>You gain +3p.`
    } else {
        gain = -3;
        message += `<br>You lose -3p.`
    }

    html = html.replace("{{MODAL_MESSAGE}}", message)
    main_text_area.append(html)

    globalThis.reward = Math.max(0, globalThis.reward + gain)

    $("#text_score").html(`Reward: 1$+${globalThis.reward}p (bonus)&nbsp;&nbsp;&nbsp;Progress: ${globalThis.data_i + 1}/${globalThis.data.length}`)

    await timer(1000)
    $("#button_ok").on("click", () => {
        // should not be necessary because the whole html in the box gets overriden
        $("#modal_dialog").remove()
        next_main_question()
    })
}

async function setup_main_question() {
    globalThis.time_start = Date.now()

    let html = await get_html("main_task.html")
    html = html.replace("{{ANSWER}}", globalThis.data_now["answer"])

    if (globalThis.data_now["mode"].includes("tags")) {
        html = html.replace("{{TAGS}}", globalThis.data_now["tags"])
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
        show_evaluation(true)
        log_data(true)
    })
    $("#button_no").on("click", () => {
        show_evaluation(false)
        log_data(false)
    })

    $("#button_no").prop('disabled', true)
    $("#button_yes").prop('disabled', true)
    await timer(5000)
    $("#button_no").prop('disabled', false)
    $("#button_yes").prop('disabled', false)
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
        html_text += `<br>Please click <a href="https://app.prolific.com/submissions/complete?cc=C6XCI3SV">this link</a> to go back to Prolific. `
        html_text += `Alternatively use this code <em>C6XCI3SV</em>.`
    }
    main_text_area.html(html_text);
}