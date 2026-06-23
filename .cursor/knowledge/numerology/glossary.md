# Numerology Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành trong hệ thống Thần Số Học (Numerology). Thần Số Học là bộ môn nghiên cứu về mối liên hệ giữa các con số và cuộc sống con người, được xây dựng trên nền tảng toán học và triết học cổ đại. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh ứng dụng trong thực tế và cách implement trong hệ thống.

## Các thuật ngữ cơ bản

### 1. Thần Số Học (神數學 - Numerology)

Thần Số Học là hệ thống nghiên cứu về ý nghĩa bí ẩn của các con số và mối liên hệ của chúng với cuộc sống con người. Hệ thống này được xây dựng trên công trình nghiên cứu của Pythagoras và các triết gia Hy Lạp cổ đại, kết hợp với các truyền thống khác từ Do Thái, Ai Cập, và Ấn Độ. Thần Số Học sử dụng ngày sinh và tên gọi để tính toán các con số chủ đạo, từ đó phân tích tính cách và vận mệnh.

Trong hệ thống, Thần Số Học được implement với nhiều phương pháp tính toán khác nhau: Phương pháp Pythagorean (phổ biến nhất ở phương Tây), Phương pháp Chaldean (cổ xưa hơn, sử dụng trong phong thủy), và các biến thể khác. Mỗi phương pháp có bảng chữ cái-numbers riêng và quy tắc tính toán riêng.

### 2. Số Chủ Đạo (命運數 - Life Path Number)

Số Chủ Đạo là con số quan trọng nhất trong Thần Số Học, được tính từ ngày sinh đầy đủ và thể hiện con đường cuộc đời mà người đó nên đi. Số Chủ Đạo cho biết bài học cuộc đời, cơ hội, thách thức, và cách để đạt được mục tiêu. Có 11 con số chủ đạo: 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, và 22 (đôi khi có 33).

Để tính Số Chủ Đạo, cộng tất cả các chữ số trong ngày sinh (ngày, tháng, năm) cho đến khi chỉ còn một chữ số hoặc một Master Number. Ví dụ người sinh 15/3/1990 có tổng: 1+5+3+1+9+9+0 = 28, tiếp tục 2+8 = 10, tiếp tục 1+0 = 1. Số Chủ Đạo là 1. Trong hệ thống, Số Chủ Đạo được tính bằng reduce function với special handling cho Master Numbers.

### 3. Số Linh Hồn (靈魂數 - Soul Urge Number)

Số Linh Hồn được tính từ nguyên âm trong tên đầy đủ và thể hiện những mong muốn sâu thẳm nhất của con người, động lực bên trong, và những gì khiến ta thực sự hạnh phúc. Số Linh Hồn cho biết điều gì thúc đẩy ta từ bên trong, những khát vọng tâm hồn, và những gì ta tìm kiếm trong cuộc sống. Đây là chỉ số về động lực nội tại chứ không phải hành động bên ngoài.

Cách tính: Lấy tất cả nguyên âm (A, E, I, O, U) trong tên đầy đủ theo giấy khai sinh, chuyển thành số theo bảng alphabet-numbers, cộng lại và rút gọn. Ví dụ tên "Nguyễn Văn An" có nguyên âm: u(3)+ê(5)+a(1)+a(1) = 10 = 1. Số Linh Hồn là 1. Trong hệ thống, cần chú ý xử lý các nguyên âm đặc biệt trong tiếng Việt như "ê", "ô", "ơ", "ư", "ươ".

### 4. Số Nhân Cách (人格數 - Personality Number)

Số Nhân Cách được tính từ phụ âm trong tên đầy đủ và thể hiện cách người khác nhìn nhận về bạn, vỏ bọc bên ngoài, và cách bạn tương tác với thế giới. Số Nhân Cách cho biết ấn tượng đầu tiên mà người khác có về bạn, những gì bạn thể hiện ra bên ngoài, và cách bạn xuất hiện trong mắt người khác. Đây là chỉ số về hình ảnh công khai chứ không phải bản chất thật.

Cách tính: Lấy tất cả phụ âm trong tên đầy đủ, chuyển thành số theo bảng alphabet-numbers, cộng lại và rút gọn. Số Nhân Cách thường được sử dụng để hiểu cách người khác nhìn nhận bạn và cách bạn nên present bản thân trong các tình huống xã hội.

### 5. Số Biểu Đạt (表達數 - Expression Number)

Số Biểu Đạt (còn gọi là Số Tài Năng) được tính từ toàn bộ tên đầy đủ và thể hiện tài năng bẩm sinh, khả năng tự nhiên, và cách bạn sử dụng năng lực của mình. Số Biểu Đạt cho biết bạn được sinh ra với những tài năng gì, bạn có thể đạt được điều gì nếu phát huy hết tiềm năng, và con đường nào có thể mang lại thành công. Đây là chỉ số về năng khiếu bẩm sinh.

Cách tính: Lấy toàn bộ tên (họ, đệm, tên) chuyển thành số theo bảng alphabet-numbers, cộng lại và rút gọn. Ví dụ "Nguyễn Văn An" = 5+7+3+5+1+5+1+1+5 = 32 = 5. Số Biểu Đạt là 5. Số Biểu Đạt cần được xem xét cùng với Số Chủ Đạo để hiểu rõ con đường phát triển bản thân.

### 6. Số Ngày Sinh (生日數 - Birth Day Number)

Số Ngày Sinh là chữ số của ngày trong tháng sinh (1-31) và thể hiện những món quà bẩm sinh bạn mang theo. Số Ngày Sinh cho biết bạn có những điểm mạnh tự nhiên nào, những gì bạn có thể đóng góp cho thế giới, và cách bạn nổi bật so với người khác. Đây là chỉ số đơn giản nhất nhưng mang ý nghĩa quan trọng vì nó không bị thay đổi bởi bất kỳ yếu tố nào khác.

Cách tính: Nếu ngày sinh là số có một chữ số (1-9), đó là Số Ngày Sinh. Nếu ngày sinh là số có hai chữ số (10-31), có thể giữ nguyên (nếu là Master Number 11, 22, 29, 31) hoặc rút gọn (10 = 1, 12 = 3, v.v.). Số Ngày Sinh không bao giờ rút gọn về một chữ số trừ khi nó là Master Number.

### 7. Số Vận Mệnh (命運數 - Destiny Number)

Số Vận Mệnh (còn gọi là Số Tên) được tính từ tên đầy đủ và thể hiện những gì bạn đã chọn trước khi sinh ra, mục tiêu cuộc đời, và con đường bạn cần đi. Số Vận Mệnh cho biết bạn đến thế giới này để làm gì, bài học cuộc đời của bạn là gì, và bạn cần đạt được điều gì. Đây là chỉ số về mục đích sống và định hướng tương lai.

Trong thực tế, Số Vận Mệnh thường được tính giống như Số Biểu Đạt vì cả hai đều sử dụng tên đầy đủ. Tuy nhiên, một số trường phái phân biệt: Số Vận Mệnh sử dụng tên khai sinh, trong khi Số Biểu Đạt có thể sử dụng tên thường dùng hoặc nickname. Trong hệ thống, cần hỏi người dùng muốn sử dụng tên nào.

### 8. Master Numbers (主數 - Master Numbers)

Master Numbers là các con số 11, 22, và 33 được coi là có năng lượng đặc biệt mạnh mẽ và không nên rút gọn. 11 là số của người có khả năng cảm nhận bằng trực giác, 22 là số của người có khả năng biến giấc mơ thành hiện thực ở quy mô lớn, 33 là số của người có khả năng tiếp nhận và truyền tải thông tin tâm linh. Master Numbers mang cả tiềm năng lớn hơn và thách thức lớn hơn.

Trong hệ thống, Master Numbers cần được xử lý đặc biệt: không rút gọn khi xuất hiện trong quá trình tính toán, và hiển thị với ý nghĩa riêng thay vì ý nghĩa của tổng các chữ số. Ví dụ 11 không chỉ là 1+1=2 mà là "Visionary" với khả năng cảm nhận siêu nhiên và tâm linh.

### 9. Số Mục Đích (目的數 - Purpose Number)

Số Mục Đích được tính từ ngày sinh và thể hiện lý do bạn đến với thế giới này. Đây là chỉ số về mục tiêu cốt lõi và ý nghĩa cuộc đời. Cách tính: Cộng tất cả các chữ số trong ngày sinh (không rút gọn từng phần mà cộng tất cả một lần) cho đến khi đạt được một chữ số hoặc Master Number.

Số Mục Đích cung cấp thông tin về: điều bạn sinh ra để làm, bài học bạn cần học, và điều bạn cần đạt được trước khi rời khỏi thế giới này. Chỉ số này thường được sử dụng cùng với Số Chủ Đạo để có bức tranh toàn diện về con đường cuộc đời.

### 10. Số Tương Sinh (相生數 - Challenge Numbers)

Số Tương Sinh là các con số thể hiện những thách thức và cơ hội trong cuộc đời. Có bốn loại: Thách Thức Căn Bản (tổng thể), Thách Thức Đầu Tiên (từ ngày và tháng), Thách Thức Giữa (từ tháng và năm), Thách Thức Cuối (từ ngày và năm). Mỗi Thách Thức thể hiện những bài học và cơ hội trong các giai đoạn khác nhau của cuộc đời.

Cách tính Thách Thức: Lấy hiệu số tuyệt đối giữa hai yếu tố, cộng các chữ số và rút gọn. Ví dụ Thách Thức Đầu Tiên = |ngày - tháng|, cộng các chữ số và rút gọn. Số Tương Sinh có thể dương (thách thức) hoặc âm (cơ hội), tùy thuộc vào việc số đó lớn hơn hay nhỏ hơn Số Chủ Đạo.

### 11. Số Đỉnh Cao (巔峰數 - Pinnacle Numbers)

Số Đỉnh Cao là các con số thể hiện những giai đoạn thịnh vượng và thành công trong cuộc đời. Có bốn Đỉnh Cao tương ứng với bốn giai đoạn: Đỉnh Cao 1 (0-28 tuổi), Đỉnh Cao 2 (28-37 tuổi), Đỉnh Cao 3 (37-55 tuổi), Đỉnh Cao 4 (55+ tuổi). Mỗi Đỉnh Cao cho biết thời gian và năng lượng của giai đoạn thịnh vượng trong cuộc đời.

Cách tính: Mỗi Đỉnh Cao được tính bằng cách cộng hai yếu tố liên quan và rút gọn. Đỉnh Cao 1 = ngày + tháng, Đỉnh Cao 2 = ngày + năm, Đỉnh Cao 3 = tháng + năm, Đỉnh Cao 4 = tổng tất cả ba Đỉnh Cao. Khi một Đỉnh Cao xuất hiện trong cuộc đời, đó là thời điểm thuận lợi để đạt được thành công trong các lĩnh vực liên quan.

### 12. Số Cân Bằng (平衡數 - Balance Number)

Số Cân Bằng được tính từ các chữ cái đầu tiên của tên đầy đủ (họ, đệm, tên) và thể hiện cách bạn tiếp cận các tình huống trong cuộc sống. Đây là chỉ số về phương pháp và chiến lược bạn sử dụng để đối mặt với thách thức. Số Cân Bằng cho biết cách bạn phản ứng khi đối diện với quyết định khó khăn và cách bạn tìm kiếm sự cân bằng trong cuộc sống.

Cách tính: Lấy chữ cái đầu tiên của mỗi tên, chuyển thành số theo bảng alphabet-numbers, cộng lại và rút gọn. Ví dụ "Nguyễn Văn An" = N(5) + V(4) + A(1) = 10 = 1. Số Cân Bằng là 1, thể hiện người có xu hướng tiếp cận vấn đề một cách độc lập và quyết đoán.

### 13. Số Trưởng Thành (成熟數 - Maturity Number)

Số Trưởng Thành được tính bằng cách cộng Số Chủ Đạo với Số Biểu Đạt và rút gọn, thể hiện những gì bạn sẽ trở thành khi trưởng thành và những bài học cuộc đời bạn sẽ tích lũy. Đây là chỉ số về sự phát triển và trưởng thành, cho biết bạn sẽ ngày càng thể hiện những phẩm chất nào khi già đi và cách những trải nghiệm sẽ định hình con người bạn.

Số Trưởng Thành thường được kích hoạt sau tuổi 40, khi con người bắt đầu hướng nội và suy ngẫm nhiều hơn. Chỉ số này cho biết: những bài học bạn sẽ học được, cách bạn sẽ thay đổi theo thời gian, và phiên bản trưởng thành nhất của bạn sẽ như thế nào.

### 14. Hạn Số (年限 - Personal Year Number)

Hạn Số là con số của năm hiện tại (hoặc bất kỳ năm nào) cho một cá nhân cụ thể, cho biết năng lượng và xu hướng của năm đó. Cách tính: Cộng năm dương lịch với Số Chủ Đạo (hoặc sử dụng phương pháp khác), rút gọn nếu cần. Hạn Số cho biết điều gì sẽ là chủ đề chính của năm và những cơ hội hay thách thức nào có thể xuất hiện.

Có 9 chu kỳ Hạn Số từ 1 đến 9, mỗi chu kỳ mang một ý nghĩa riêng: Hạn Số 1 là năm của khởi đầu và độc lập, Hạn Số 2 là năm của hợp tác và cân bằng, Hạn Số 3 là năm của sáng tạo và giao tiếp, v.v. Khi Hạn Số là Master Number (11, 22, 33), năm đó có ý nghĩa đặc biệt mạnh mẽ.

### 15. Bảng Chữ Cái-Numbers (字母表 - Alphabet Chart)

Bảng Chữ Cái-Numbers là bảng gán số cho các chữ cái trong bảng alphabet, được sử dụng để tính toán các chỉ số từ tên. Có nhiều phương pháp: Phương pháp Pythagorean sử dụng bảng 1-9 lặp lại (A=1, B=2, C=3... I=9, J=1, K=2...). Phương pháp Chaldean sử dụng bảng 1-8 (A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9...).

Trong hệ thống, cần hỗ trợ cả hai phương pháp và cho phép người dùng chọn. Đối với tiếng Việt, cần có bảng chuyển đổi từ chữ cái Việt Nam sang alphabet tiếng Anh trước khi tra bảng. Ví dụ "Ê" được chuyển thành "E", "Ô" thành "O", "Đ" thành "D".

### 16. Số May Mắn (幸運數 - Lucky Numbers)

Số May Mắn là các con số được xác định dựa trên Thần Số Học của một người và có thể mang lại may mắn trong cuộc sống hàng ngày. Cách xác định: Dựa trên Số Chủ Đạo và các chỉ số khác, xác định các con số có năng lượng tương thích. Số May Mắn có thể được sử dụng trong: chọn ngày quan trọng, chọn số điện thoại, số nhà, biển số xe, số tài khoản.

Trong hệ thống, Số May Mắn được xác định từ: Số Chủ Đạo (số chính), các con số liên quan trong lá số, và các con số có ý nghĩa trong ngũ hành tương ứng. Nên cung cấp danh sách các Số May Mắn kèm theo giải thích về ý nghĩa và cách sử dụng.

### 17. Số Lặp (重複數 - Repeating Numbers)

Số Lặp là các con số xuất hiện nhiều lần trong ngày sinh hoặc tên, được coi là có ý nghĩa đặc biệt. Khi một số xuất hiện nhiều lần, năng lượng của số đó được усилен. Ví dụ người sinh ngày 11/11/1991 có Số 1 xuất hiện 4 lần và Số 9 xuất hiện 2 lần. Số Lặp có thể cho biết: điểm mạnh đặc biệt, bài học cần học, hoặc chủ đề xuyên suốt cuộc đời.

Trong hệ thống, cần đếm tần suất xuất hiện của mỗi chữ số trong ngày sinh và tên. Các số xuất hiện 2 lần trở lên được coi là Số Lặp và cần được highlight trong phân tích. Số xuất hiện 3 lần trở lên có ý nghĩa đặc biệt mạnh mẽ.

### 18. Triangular Numbers (三角數 - Triangular Numbers)

Triangular Numbers trong Thần Số Học là các số có thể được biểu diễn dưới dạng tam giác đều (1, 3, 6, 10, 15, 21, 28...). Các số này được coi là có ý nghĩa đặc biệt vì chúng xuất phát từ phương pháp của Pythagoras. Khi ngày sinh hoặc tổng các chữ số tạo thành Triangular Number, điều đó được coi là có ý nghĩa đặc biệt về mặt tâm linh.

Trong hệ thống, khi phát hiện Triangular Number, cần highlight và cung cấp giải thích về ý nghĩa đặc biệt. Triangular Numbers có thể xuất hiện trong: Số Chủ Đạo, tổng ngày sinh, hoặc các tổng khác trong lá số.

## Kết luận

Từ điển thuật ngữ này cung cấp nền tảng kiến thức vững chắc về các khái niệm trong Thần Số Học. Việc hiểu rõ từng thuật ngữ và mối quan hệ giữa chúng là điều kiện tiên quyết để xây dựng hệ thống Thần Số Học chính xác và có giá trị. Các developers nên tham khảo các tài liệu chuyên sâu và hợp tác với các chuyên gia Thần Số Học để đảm bảo độ chính xác trong implementation.
