// implementation of printf for use in Arduino sketch
void Serial_printf(char* fmt, ...) {
    char buf[512]; // resulting string limited to 256 chars
    va_list args;
    va_start (args, fmt );
    vsnprintf(buf, 512, fmt, args);
    va_end (args);
    Serial.print(buf);
}

// simple URL encoder
String urlEncode(const char* msg)
{
    static const char hex[] = "0123456789abcdef";
    String encodedMsg = "";

    while (*msg!='\0'){
        if( ('a' <= *msg && *msg <= 'z')
            || ('A' <= *msg && *msg <= 'Z')
            || ('0' <= *msg && *msg <= '9') ) {
            encodedMsg += *msg;
        } else {
            encodedMsg += '%';
            encodedMsg += hex[*msg >> 4];
            encodedMsg += hex[*msg & 15];
        }
        msg++;
    }
    return encodedMsg;
}

// int32_t indexOf(const char* buffer, size_t length, const char* look_for, size_t look_for_length, int32_t start_index) {
//     if (look_for_length > length) {
//         return -1;
//     }

//     for (size_t pos = start_index; pos < length; pos++) {
//         if (length - pos < look_for_length) {
//             return -1;
//         }

//         if (buffer[pos] == *look_for) {
//             size_t sub = 1;
//             for (; sub < look_for_length; sub++) {
//                 if (buffer[pos + sub] != look_for[sub]) break;
//             }

//             if (sub == look_for_length) {
//                 return pos;
//             }
//         }
//     }

//     return -1;
// }