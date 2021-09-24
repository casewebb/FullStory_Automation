class Locator(object):
    link_by_text = "//*[self::a or self::span or self::button][contains(text(),'{link_text}')]"
    input_by_placeholder = "//input[@placeholder='{placeholder_text}']"
    input_by_section_and_label = "//h3[text()='{section_text}']/following-sibling::form[1]//label[text()='{" \
                                 "label_text}']/following-sibling::input"
    select_by_section_and_label = "//h3[text()='{section_text}']/following-sibling::form[1]//label[text()='{" \
                                  "label_text}']/following-sibling::select" \
                                  "| //h3[text()='{section_text}']/following-sibling::form[1]//div//label[text()='{" \
                                  "label_text}']//parent::div/following-sibling::select"
    checkbox_by_label = "//label[contains(normalize-space(.),'{label_text}')]"
