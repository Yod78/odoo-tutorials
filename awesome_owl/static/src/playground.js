import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {};
    static components = { Counter, Card };

    htmlContent = markup("<b>Je suis en gras</b>");
    escapedContent = "<b>pas de gras</b>";

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}