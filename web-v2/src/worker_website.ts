import { log_data, get_json, get_html } from "./connector";
import { DEVMODE } from "./globals";
import { timer } from "./utils";

let main_text_area = $("#main_text_area")

export async function setup_intro_information_1() {
    // hide for now
    $("#short_instructions").toggle(false)
    main_text_area.html(await get_html("instructions_1.html"))
    await timer(10)
    $("#button_start").on("click", setup_intro_information_2)
}

export async function setup_intro_information_2() {
    main_text_area.html(await get_html("instructions_2.html"))
    await timer(10)
    $("#button_start").on("click", setup_intro_information_3)
}

export async function setup_intro_information_3() {
    main_text_area.html(await get_html("instructions_3.html"))
    await timer(10)
    $("#button_start").on("click", setup_intro_information_4)
}

export async function setup_intro_information_4() {
    main_text_area.html(await get_html("instructions_4.html"))
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

let message_history = ""

async function show_evaluation(response: Boolean) {
    let correct = globalThis.data_now["correct"]
    let html = await get_html("modal_response.html")
    let text_correct = "<span class='span_correct'>correct</span>"
    let text_incorrect = "<span class='span_incorrect'>incorrect</span>"
    let message = ""
    if (!globalThis.data_now["reveal"]) {
        message = `You answered that the AI was ${response ? text_correct : text_incorrect}.`
    } else {
        if (response == correct) {
            message = `You answered that the AI was ${response ? text_correct : text_incorrect} and the AI was in fact ${correct ? text_correct : text_incorrect},`
        } else {
            message = `You answered that the AI was ${response ? text_correct : text_incorrect} but the AI was in fact ${correct ? text_correct : text_incorrect}.`
        }

        // update history
        let message_history_local = "<em>" + globalThis.data_now["answer"] + "</em><br>";
        if (globalThis.data_now["mode"].includes("tags")) {
            message_history_local += globalThis.data_now["tags"].replace("This fact is about", "This fact was about");
        }
        message_history_local += `You answered that the AI was ${response ? text_correct : text_incorrect} and the AI was ${correct ? text_correct : text_incorrect}.`
        message_history = `${message_history_local}<hr>${message_history}`
        $("#short_instructions").html(
            `<h3>History:</h3><hr>` +
            message_history
        )
    }

    // compute reward
    let gain = 0
    if (correct == response) {
        gain += 2;
        message += `<br>You gain +2p.`
    } else {
        gain = -2;
        message += `<br>You lose -2p.`
    }


    html = html.replace("{{MODAL_MESSAGE}}", message)
    main_text_area.append(html)

    globalThis.reward = Math.max(0, globalThis.reward + gain)

    if (globalThis.data_now["reveal"]) {
        $("#text_score").html(`Reward: 1$+${globalThis.reward}p (bonus)&nbsp;&nbsp;&nbsp;Progress: ${globalThis.data_i + 1}/${globalThis.data.length}`)
    } else {
        $("#text_score").html(`Reward: 1$+[hidden]p (bonus)&nbsp;&nbsp;Progress: ${globalThis.data_i + 1}/${globalThis.data.length}`)
    }

    if (!globalThis.skip_intro) {
        await timer(1000)
    }
    $("#button_ok").on("click", () => {
        // should not be necessary because the whole html in the box gets overriden
        $("#modal_dialog").remove()
        next_main_question()
    })
}

export async function setup_main_question() {
    globalThis.time_start = Date.now()

    // show short instructions
    $("#short_instructions").toggle(true)

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
    if (!globalThis.skip_intro) {
        await timer(2000)
    }
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
        html_text += `<br>Please click <a class="button_like" href="https://app.prolific.com/submissions/complete?cc=C6XCI3SV">this link</a> to go back to Prolific. `
        html_text += `Alternatively use this code <em>C6XCI3SV</em>.`
    }
    main_text_area.html(html_text);
}